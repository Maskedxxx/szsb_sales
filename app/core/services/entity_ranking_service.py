# app/core/services/entity_ranking_service.py

from dataclasses import dataclass
import json
import logging
from typing import Dict, List, Optional, Mapping, Sequence, Union
# ValidationError больше не используется с динамической моделью
from app.core.service_models import EntityRankingModel

@dataclass
class EntityRankingConfig:
    """Configuration for entity ranking process."""
    model_name: str
    temperature: float = 0
    max_retries: int = 2
    max_tokens: int = 4096
    entity_type: str = "entity"  # "route" или "key"
    subsector_id: Optional[str] = None  # Добавляем ID подсектора
    context_hints: Optional[str] = None  # Добавляем контекстные подсказки

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
        formatted_lines = []
        entity_names = []
        
        if isinstance(entities, Mapping):
            # dict: entity -> description
            for i, (name, desc) in enumerate(entities.items(), 1):
                formatted_lines.append(
                    f"{i}. entities_name --> <{name}>, entities_description --> \"{desc}\""
                )
                entity_names.append(f"<{name}>")
        else:
            # sequence of dicts
            for i, r in enumerate(entities, 1):
                entity_name = r.get('entity', r.get('route', ''))
                description = r.get('description', '')
                formatted_lines.append(
                    f"{i}. entities_name --> <{entity_name}>, entities_description --> \"{description}\""
                )
                entity_names.append(f"<{entity_name}>")
        
        # Добавляем напоминание в конец
        entities_reminder = f"\nВнимание! Напоминаю вам список entity_name для оценки: [{', '.join(entity_names)}]"
        
        return "\n".join(formatted_lines) + entities_reminder

    def _filter_context_hints(self, context_hints: str, allowed_entities: List[str]) -> str:
        """
        Фильтрует context hints, оставляя только строки для разрешенных сущностей.
        
        Args:
            context_hints: Полный текст контекстных подсказок
            allowed_entities: Список разрешенных имен сущностей
            
        Returns:
            Отфильтрованные context hints только для разрешенных сущностей
        """
        if not context_hints or not allowed_entities:
            return context_hints or ""
            
        lines = context_hints.split('\n')
        filtered_lines = []
        current_entity = None
        
        for line in lines:
            # Проверяем, является ли строка началом описания сущности (формат: "entity_name: ")
            stripped = line.strip()
            if ':' in stripped and not stripped.startswith('ВАЖНО'):
                # Извлекаем имя сущности (все до первого двоеточия)
                entity_name = stripped.split(':')[0].strip()
                if entity_name in allowed_entities:
                    current_entity = entity_name
                    filtered_lines.append(line)
                else:
                    current_entity = None
            else:
                # Если мы внутри разрешенной сущности или это общая строка, добавляем
                if current_entity is not None or not stripped or stripped.startswith('ВАЖНО'):
                    filtered_lines.append(line)
        
        filtered_hints = '\n'.join(filtered_lines)
        self.logger.info(f"Filtered context hints for entities: {allowed_entities}")
        self.logger.debug(f"Original hints length: {len(context_hints)}, Filtered length: {len(filtered_hints)}")
        
        return filtered_hints

    def _log_response_obj(self, obj_str: str):
        """Log the fields of the response model object"""
        self.logger.info(f"EntityRanking response: \n {json.dumps(json.loads(obj_str), indent=4, ensure_ascii=False)}")

    def _prepare_messages(self, query, entities_with_descriptions: str, allowed_entities: List[str]) -> List[Dict[str, str]]:
        """Prepare messages for LLM prompt."""
        
        # Фильтруем context hints только для разрешенных сущностей
        filtered_context_hints = self._filter_context_hints(
            self.config.context_hints or "", 
            allowed_entities
        )
        
        system_prompt = self.prompt_template.system
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": self.prompt_template.user.format(
                query=query, 
                entities=entities_with_descriptions,
                entity_type=self.config.entity_type,
                context_hints=filtered_context_hints
            )}
        ]


    def _get_model_response_structured(
            self,
            messages: List[Dict[str, str]]
    ) -> Optional[Dict]:
        """Get model response using static structured model."""
        response = self.client.beta.chat.completions.parse(
            temperature=self.config.temperature,
            model=self.config.model_name,
            messages=messages,
            response_format=EntityRankingModel,
            max_tokens=self.config.max_tokens
        )

        if response.choices and response.choices[0].message:
            self._log_response_obj(response.choices[0].message.content)
            return response.choices[0].message
        else: 
            return None

    def _process_response(self, response: Optional[dict], allowed_entities: List[str], top_n: int = 1)-> List[str]:
        """Process and validate model response."""
        if not response:
            return []

        if response.refusal:
            self.logger.warning(f"Model refused to rank: {response.refusal}")
            return []

        try:
            # Очищаем имена сущностей от специальных символов (#, <, >)
            if response.parsed and hasattr(response.parsed, 'entity_scores'):
                cleaned_entity_scores = {}
                for key, value in response.parsed.entity_scores.items():
                    # Удаляем #, <, > из имени сущности
                    cleaned_key = key.replace('#', '').replace('<', '').replace('>', '')
                    cleaned_entity_scores[cleaned_key] = value
                
                # Заменяем оригинальные entity_scores на очищенные
                response.parsed.entity_scores = cleaned_entity_scores
                
                self.logger.info(f"Cleaned entity names from special characters: {list(cleaned_entity_scores.keys())}")
                
            # Фильтруем ответ - оставляем только разрешенные сущности
            raw_entity_scores = response.parsed.entity_scores
            
            # Оставляем только сущности из allowed_entities
            entity_scores = {
                entity: score for entity, score in raw_entity_scores.items() 
                if entity in allowed_entities
            }
            
            if not entity_scores:
                self.logger.warning(f"No valid entities found in response. Raw: {list(raw_entity_scores.keys())}, Allowed: {allowed_entities}")
                return []
                
            if len(entity_scores) != len(raw_entity_scores):
                filtered_out = set(raw_entity_scores.keys()) - set(entity_scores.keys())
                self.logger.info(f"Filtered out invalid entities: {list(filtered_out)}")
            
            # Сортируем сущности по оценке и берем top_n
            sorted_entities = sorted(
                entity_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            selected_entities = [entity for entity, _ in sorted_entities[:top_n]]
            
            self.logger.info(f"Selected top {top_n} entities: {selected_entities}")
            self.logger.info(f"All scores: {entity_scores}")
            
            return selected_entities
            
        except Exception as e:
            self.logger.error(f"Response processing failed: {e}")
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
            
            # Получаем список разрешённых сущностей
            allowed_entities = (
                list(entities.keys())                   # dict-format
                if isinstance(entities, Mapping)
                else [e.get("entity", e.get("route", "")) for e in entities]  # list-of-dict
            )
            
            # Подготавливаем сообщения с отфильтрованными context hints
            messages = self._prepare_messages(query, entities_with_descriptions, allowed_entities)
            
            # Используем статическую модель, фильтрация происходит через context hints и post-processing
            response = self._get_model_response_structured(messages)
            return self._process_response(response, allowed_entities, top_n)
        
        except Exception as e:
            self.logger.error(f"Failed to rank entities: {e}")
            return []