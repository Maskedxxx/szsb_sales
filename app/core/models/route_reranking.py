from typing import List
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from utils.logger import logger

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
    description="Краткая причина выбора такой последовательности маршрутов и почему их содержания релевантно для создания ответа пользователю"
    )
    reranked_routes: List[str] = Field(
        ...,
        max_items=MAX_ROUTES,
        description="""Полное название / имя выбранного маршрута без его описания!
        Названия разделенные `_` (подчеркиванием) не делить на состовляющие!"""
    )


class RouteRerankingValidationModel(BaseModel):
    reranked_routes: List[str]
    reasoning_step_by_step: List[str]
    reason: str

    @field_validator('reranked_routes')
    @classmethod
    def validate_selected_routes(cls, value: List[str], info: ValidationInfo) -> List[str]:
        allowed_routes = info.context.get("allowed_routes", []) if info.context else []
        if not value:
            raise ValueError(f"RouteRerankingModel returned no routes")
            
        common_elements = list(set(value) & set(allowed_routes))
        if not common_elements:
            raise ValueError(f"No common allowed routes!\nReranked: {value}.\nAllowed: {allowed_routes}")

        if len(common_elements) != len(value):
            logger.info(f"Not all retrieved routes are allowed!\nRetrieved: {value}\nAllowed: {allowed_routes}")

        return common_elements

