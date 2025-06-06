from typing import List, Dict
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from app.utils import logger

MIN_ROUTES = 1
MAX_ROUTES = 20  # Увеличим до 5, т.к. теперь мы оцениваем все роуты
MIN_REASONING_STEPS = 1
MAX_REASONING_STEPS = 3

class EntityRankingParseModel(BaseModel):
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
        description="""Dictionary where the key is the entity name and the value is a confidence score from 0 to 1.
        Names separated by `_` (underscore) should not be divided into components! Maximum 5 entity in dict for eval"""
    )


class EntityRankingValidationModel(BaseModel):
    entity_scores: Dict[str, float]
    reasoning_step_by_step: List[str]
    reason: str

    @field_validator('entity_scores')
    @classmethod
    def validate_entity_scores(cls, value: Dict[str, float], info: ValidationInfo) -> Dict[str, float]:
        allowed_entities = info.context.get("allowed_entities", []) if info.context else []
        if not value:
            raise ValueError(f"EntityRankingModel returned no entities")
            
        # Проверяем, что все сущности из ответа есть в списке разрешенных
        valid_entities = {k: v for k, v in value.items() if k in allowed_entities}
        
        if not valid_entities:
            raise ValueError(f"No common allowed entities!\nScored: {list(value.keys())}.\nAllowed: {allowed_entities}")

        if len(valid_entities) != len(value):
            logger.info(f"Not all scored entities are allowed!\nScored: {list(value.keys())}\nAllowed: {allowed_entities}")

        return valid_entities