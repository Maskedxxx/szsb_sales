from typing import List
from pydantic import BaseModel, Field, ValidationInfo, field_validator

MIN_ROUTES=1
MAX_ROUTES=3
MIN_REASONING_STEPS=1
MAX_REASONING_STEPS=3

class RouteRerankingParseModel(BaseModel):
    reasoning_step_by_step: List[str] = Field(
    ...,
    min_items=MIN_REASONING_STEPS,
    max_items=MAX_REASONING_STEPS,
    description="Массив строк с пошаговым рассуждением. Каждый элемент должен быть полным предложением."
    )
    reason: str = Field(
        ...,
        description="Краткая причина выбора такого ранжирования маршрутов"
    )
    reranked_routes: List[str] = Field(
        ...,
        max_items=MAX_ROUTES,
        description="Полное название / имя выбранного маршрута без его описания!"
    )


class RouteRerankingValidationModel(BaseModel):
    reranked_routes: List[str]
    reasoning_step_by_step: List[str]
    reason: str

    @field_validator('reranked_routes')
    @classmethod
    def validate_selected_routes(cls, value: List[str], info: ValidationInfo) -> List[str]:
        allowed_routes = info.context.get("allowed_routes", []) if info.context else []
        if not value or not set(value).issubset(allowed_routes):
            raise ValueError(f"Invalid route: {value}. Must be a subset of {allowed_routes}")
        return value

