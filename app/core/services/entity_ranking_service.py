from dataclasses import dataclass
import json
import logging
from typing import Dict, List, Optional, Mapping, Sequence, Union
from pydantic import ValidationError
from app.core.service_models import EntityRankingParseModel, EntityRankingValidationModel

@dataclass
class EntityRankingConfig:
    """Configuration for entity ranking process."""
    model_name: str
    temperature: float = 0
    max_retries: int = 2
    max_tokens: int = 4096
    entity_type: str = "entity"  # "route" или "key"

@dataclass
class EntityRankingPromptTemplate:
    """Template for LLM prompts."""
    system: str
    user: str

class EntityRankingService:
    """Service for ranking entities using LLM."""

    def __init__(
        self,
        client,
        config: EntityRankingConfig,
        prompt_template: EntityRankingPromptTemplate, 
        logger
    ):
        self.client = client
        self.config = config
        self.prompt_template = prompt_template
        self.logger = logger or logging.getLogger(__name__)

    def _format_entities_with_descriptions(
        self,
        entities: Union[Mapping[str, str], Sequence[Dict[str, str]]]
    ) -> str:
        """
        Format entities with descriptions for the prompt.
        Supports both formats:
        1. {"entity_name": "description", ...}
        2. [{"entity": "...", "description": "..."}, ...]
        """
        if isinstance(entities, Mapping):
            # dict: entity -> description
            return "\n".join(
                f"- #{name}#: \"{desc}\""
                for name, desc in entities.items()
            )
        # sequence of dicts
        return "\n".join(
            f"- #{r.get('entity', r.get('route', ''))}#: \"{r.get('description', '')}\""
            for r in entities
        )

    def _log_response_obj(self, obj_str: str):
        """Log the fields of the response model object"""
        self.logger.info(f"EntityRanking response: \n {json.dumps(json.loads(obj_str), indent=4, ensure_ascii=False)}")

    def _prepare_messages(
            self,
            query,
            entities_with_descriptions: str
    ) -> List[Dict[str, str]]:
        """Prepare messages for LLM prompt."""
        return [
            {"role": "system", "content": self.prompt_template.system},
            {"role": "user", "content": self.prompt_template.user.format(
                query=query, 
                entities=entities_with_descriptions,
                entity_type=self.config.entity_type
            )}
        ]

    def _get_model_response(
            self,
            messages: List[Dict[str, str]]
    ) -> Optional[Dict]:
        """Get model response."""
        response = self.client.beta.chat.completions.parse(
            temperature=self.config.temperature,
            model=self.config.model_name,
            messages=messages,
            response_format=EntityRankingParseModel,
            max_tokens=self.config.max_tokens
        )

        if response.choices and response.choices[0].message:
            self._log_response_obj(response.choices[0].message.content)
            return response.choices[0].message
        else: 
            return None

    def _process_response(
        self,
        response: Optional[dict],
        allowed_entities: List[str],
        top_n: int = 1
    )-> List[str]:
        """Process and validate model response."""
        if not response:
            return []

        if response.refusal:
            self.logger.warning(f"Model refused to rank: {response.refusal}")
            return []

        try:
            validated = EntityRankingValidationModel.model_validate(
                obj=response.parsed.model_dump(),
                context={"allowed_entities": allowed_entities}
            )
            
            # Сортируем сущности по оценке и берем top_n
            sorted_entities = sorted(
                validated.entity_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            selected_entities = [entity for entity, _ in sorted_entities[:top_n]]
            
            self.logger.info(f"Selected top {top_n} entities: {selected_entities}")
            self.logger.info(f"All scores: {validated.entity_scores}")
            
            return selected_entities
            
        except ValidationError as e:
            self.logger.error(f"Response validation failed: {e}")
            return []

    def rank_entities(
            self,
            query: str,
            entities: Dict[str, str],
            top_n: int = 1
    ) -> List[str]:
        """
        Rank entities based on relevance to query and return top N.
        
        Args:
            query: User query text
            entities: Dictionary mapping entity names to descriptions
            top_n: Number of top entities to return
            
        Returns:
            List of top N entity names ranked by relevance
        """
        try:
            entities_with_descriptions = self._format_entities_with_descriptions(entities)
            messages = self._prepare_messages(query, entities_with_descriptions)
            response = self._get_model_response(messages)
            allowed_entities = (
                list(entities.keys())                   # dict-format
                if isinstance(entities, Mapping)
                else [e.get("entity", e.get("route", "")) for e in entities]  # list-of-dict
            )

            return self._process_response(response, allowed_entities, top_n)
        
        except Exception as e:
            self.logger.error(f"Failed to rank entities: {e}")
            return []