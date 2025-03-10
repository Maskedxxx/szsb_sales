from typing import List
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from utils.logger import logger

MIN_KEYS=1
MAX_KEYS=2
MIN_REASONING_STEPS=1
MAX_REASONING_STEPS=3

class KeySelectionParseModel(BaseModel):
    reasoning_step_by_step: List[str] = Field(
    ..., 
    min_items=MIN_REASONING_STEPS, 
    max_items=MAX_REASONING_STEPS, 
    description="Массив строк с пошаговым рассуждением. Каждый элемент должен быть полным предложением."
    )
    reason: str = Field(
    ...,
    description="Краткая причина выбора таких ключей и почему их содержания релевантно для создания ответа пользователю"
    )
    selected_keys: List[str] = Field(
        ..., 
        min_items=MIN_KEYS,
        max_items=MAX_KEYS,
        description="""Полное название / имя выбранного ключа без его описания!
        Названия разделенные `_` (подчеркиванием) не делить на состовляющие!"""
    )


class KeySelectionValidationModel(BaseModel):
    selected_keys: List[str]
    reasoning_step_by_step: List[str]

    @field_validator('selected_keys')
    @classmethod
    def validate_selected_key(cls, value: List[str], info: ValidationInfo):
        allowed_keys = info.context.get("allowed_routes", []) if info.context else []
        if not value:
            raise ValueError(f"KeySelectionModel returned no routes")
            
        common_elements = list(set(value) & set(allowed_keys))
        if not common_elements:
            raise ValueError(f"No common allowed keys!\nReranked: {value}.\nAllowed: {allowed_keys}")

        if len(common_elements) != len(value):
            logger.info(f"Not all retrieved keys are allowed!\nRetrieved: {value}\nAllowed: {allowed_keys}")

        return common_elements