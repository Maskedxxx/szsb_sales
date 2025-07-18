# app/core/service_models/reranking_model.py

from typing import List, Dict, Literal, Type
from pydantic import BaseModel, Field, create_model

MIN_ROUTES = 1
MAX_ROUTES = 20  # Увеличим до 5, т.к. теперь мы оцениваем все роуты
MIN_REASONING_STEPS = 1
MAX_REASONING_STEPS = 3

# Устаревшие классы удалены - теперь используется динамическая модель create_dynamic_entity_ranking_model()


# Простая статическая модель без Literal ограничений - фильтрация через context hints
class EntityRankingModel(BaseModel):
    reasoning_step_by_step: List[str] = Field(
        ...,
        min_length=MIN_REASONING_STEPS,
        max_length=MAX_REASONING_STEPS,
        description="List Brief reason for the entity ranking and why their content is relevant for creating a response to the user"
    )
    reason: str = Field(
        ...,
        description="Brief reason for the entity ranking and why their content is relevant for creating a response to the user"
    )
    entity_scores: Dict[str, float] = Field(
        ...,
        max_length=MAX_ROUTES,
        description="Dictionary where the key is the entity name and the value is a confidence score from 0 to 1. Names separated by `_` (underscore) should not be divided into components!"
    )