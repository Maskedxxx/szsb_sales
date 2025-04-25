# app/core/services/reranking_service.py

from dataclasses import dataclass
import json
import logging
from typing import Dict, List, Optional, Mapping, Sequence, Optional, Union
from pydantic import ValidationError
from app.core.service_models import RouteRerankingParseModel, RouteRerankingValidationModel
from app.data import PROMPT_RERANK_ROU

@dataclass
class RerankingConfig:
    """Configuration for key selection process."""
    model_name: str
    temperature: float = 0
    max_retries: int = 2
    max_tokens: int = 4096

@dataclass
class RerankingPromptTemplate:
    """Template for LLM prompts."""
    system: str
    user: str

class RerankingService:

    def __init__(
        self,
        client,
        config: RerankingConfig,
        prompt_template: RerankingPromptTemplate, 
        logger
    ):
        self.client = client
        self.config = config
        self.prompt_template = prompt_template
        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def _format_routes_with_descriptions(
        routes: Union[Mapping[str, str], Sequence[Dict[str, str]]]
    ) -> str:
        """
        Привести маршруты к тексту для промпта.

        Поддерживаются оба формата:
        1. {"route_name": "description", ...}
        2. [{"route": "...", "description": "..."}, ...]
        """
        if isinstance(routes, Mapping):
            # dict: route -> description
            return "\n".join(
                f"Маршрут: {name}; Описание: {desc}"
                for name, desc in routes.items()
            )
        # последовательность dict'ов
        return "\n".join(
            f"Маршрут: {r['route']}; Описание: {r['description']}"
            for r in routes
        )

    def _log_response_obj(self, obj_str: str):
        """Log the fields of the response model object"""
        self.logger.info(f"RouteReranking response: \n {json.dumps(json.loads(obj_str), indent=4, ensure_ascii=False)}")

    def _prepare_messages(
            self,
            query,
            routes_with_descriptions: str
    ) -> List[Dict[str, str]]:
        """Prepare messages for LLM prompt."""
        return [
            {"role": "system", "content": PROMPT_RERANK_ROU["system"]},
            {"role": "user", "content": PROMPT_RERANK_ROU["user"].format(
                query=query, 
                routes=routes_with_descriptions
            )}
    ]

    def _get_model_response(
            self,
            messages: List[Dict[str, str]]
    ) -> Optional[Dict]:
        response = self.client.beta.chat.completions.parse(
            temperature=self.config.temperature,
            model=self.config.model_name,
            messages=messages,
            response_format=RouteRerankingParseModel,
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
        allowed_routes: List[str]
    )-> List[str]:
        """Process and validate model response."""
        if not response:
            return []

        if response.refusal:
            self.logger.warning(f"Model refused to rerank: {response.refusal}")
            return []

        try:
            validated = RouteRerankingValidationModel.model_validate(
                obj=response.parsed.model_dump(),
                context={"allowed_routes": allowed_routes}
            )
            self.logger.info(f"Reranked routes: {validated.reranked_routes}")
            return validated.reranked_routes
        except ValidationError as e:
            self.logger.error(f"Response validation failed: {e}")
            return []

    def rerank_routes(
            self,
            query: str,
            routes: Dict[str, str]
    ) -> List[str]:

        try:
            routes_with_descriptions = self._format_routes_with_descriptions(routes=routes)
            messages = self._prepare_messages(query, routes_with_descriptions)
            response = self._get_model_response(messages)
            allowed_routes = (
                list(routes.keys())                # dict-формат
                if isinstance(routes, Mapping)
                else [r["route"] for r in routes]  # list-of-dict
            )

            return self._process_response(response, allowed_routes)
        
        except Exception as e:
            self.logger.error(f"Failed to rerank routes: {e}")

            return []