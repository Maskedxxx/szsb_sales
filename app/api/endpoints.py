
from typing import List

from fastapi import APIRouter, HTTPException
from api.models import Subsector, Response, Query
from data.subsectors import SUBSECTORS
from core.engine import handle_query

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/subsectors", response_model=List[Subsector])
async def get_subsectors() -> List[Subsector]:
    """
    Получает список всех доступных отраслей.

    Returns:
        List[Subsector]: Список отраслей с их идентификаторами.
    """
    return [Subsector(**subsector) for subsector in SUBSECTORS]


@router.post("/process_query", response_model=Response)
async def process_query(query: Query) -> Response:
    """
    Обрабатывает запрос пользователя, выполняет семантический поиск и генерирует ответ.
    """
    try:
        return await handle_query(query)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=str(e)) from e
