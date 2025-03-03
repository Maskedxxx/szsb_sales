from typing import List
from pydantic import BaseModel, Field, ValidationInfo, field_validator

MIN_KEYS=1
MAX_KEYS=3
MIN_REASONING_STEPS=1
MAX_REASONING_STEPS=3

class KeySelectionParseModel(BaseModel):
    keys: List[str] = Field(
        ..., 
        min_items=MIN_KEYS,
        max_items=MAX_KEYS,
        description="Полное название / имя выбранного ключа без его описания! Должен содержать ровно один элемент."
    )
    reasoning_step_by_step: List[str] = Field(
        ..., 
        min_items=MIN_REASONING_STEPS, 
        max_items=MAX_REASONING_STEPS, 
        description="Массив строк с пошаговым рассуждением. Каждый элемент должен быть полным предложением."
    )

class KeySelectionValidationModel(BaseModel):
    keys: List[str]
    reasoning_step_by_step: List[str]

    @field_validator('keys')
    @classmethod
    def validate_selected_key(cls, value: List[str], info: ValidationInfo):
        allowed_keys = info.context.get("allowed_keys", []) if info.context else []
        if not value or value[0] not in allowed_keys:
            raise ValueError(f"Invalid key: {value}. Must be one of {allowed_keys}")
        return value