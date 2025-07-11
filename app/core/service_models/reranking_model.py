# app/core/service_models/reranking_model.py

from typing import List, Dict, Literal, Type
from pydantic import BaseModel, Field, create_model

MIN_ROUTES = 1
MAX_ROUTES = 20  # Увеличим до 5, т.к. теперь мы оцениваем все роуты
MIN_REASONING_STEPS = 1
MAX_REASONING_STEPS = 3

# Устаревшие классы удалены - теперь используется динамическая модель create_dynamic_entity_ranking_model()


def create_dynamic_entity_ranking_model(allowed_entities: List[str]) -> Type[BaseModel]:
    """
    Создает динамическую Pydantic модель с Literal полем для entity_scores,
    ограниченным только разрешенными сущностями.
    
    Args:
        allowed_entities: Список разрешенных имен сущностей
        
    Returns:
        Динамическая Pydantic модель для entity ranking
    """
    if not allowed_entities:
        raise ValueError("allowed_entities не может быть пустым")
        
    # Создаем Literal тип для разрешенных сущностей
    if len(allowed_entities) == 1:
        EntityLiteral = Literal[allowed_entities[0]]
    else:
        EntityLiteral = Literal[tuple(allowed_entities)]
    
    # Создаем динамическую модель
    DynamicEntityRankingModel = create_model(
        'DynamicEntityRankingModel',
        reasoning_step_by_step=(
            List[str], 
            Field(
                ...,
                min_length=MIN_REASONING_STEPS,
                max_length=MAX_REASONING_STEPS,
                description="List Brief reason for the entity ranking and why their content is relevant for creating a response to the user"
            )
        ),
        reason=(str, Field(...,
                description="Brief reason for the entity ranking and why their content is relevant for creating a response to the user"
            )
        ),
        entity_scores=(
            Dict[EntityLiteral, float], Field(...,
                max_length=MAX_ROUTES,
                description=f"""Dictionary where the key must be one of {allowed_entities} and the value is a confidence score from 0 to 1.
                ВАЖНО: Используйте ТОЛЬКО эти имена сущностей: {', '.join(allowed_entities)}
                Names separated by `_` (underscore) should not be divided into components! Maximum {len(allowed_entities)} entity in dict for eval"""
            )
        ),
        __base__=BaseModel
    )
    
    return DynamicEntityRankingModel