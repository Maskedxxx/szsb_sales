
import asyncio
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from api.models import Subsector, Response, Query
from data.subsectors import SUBSECTORS
from utils.logger import logger
from core.engine import handle_query

router = APIRouter(prefix="/api/v1")

@router.get("/health",
            summary="Health Check",
            description="Checks the health status of the API",
            )
async def health():
    return {"status": "ok"}


@router.get("/subsectors",
            response_model=List[Subsector],
            summary="Gets subsectors list",
            description="Fetches the list of all available subsectors")
async def get_subsectors() -> List[Subsector]:
    """
    Retrieves the list of all available subsectors.
    
    Returns:
        List[Subsector]: List of subsectors with their identifiers.
    
    Raises:
        HTTPException: If there's an error fetching the subsectors.
    """

    try:
        return [Subsector(**subsector) for subsector in SUBSECTORS]
    except Exception as e:
        logger.error(f"Error fetching subsectors: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch subsectors"
        ) from e


@router.post("/process_query",
            response_model=Response,
            summary="Processes users input",
            description="Processes a user query, performs semantic search, and generates a response.")
async def process_query(query: Query) -> Response:
    """
    Processes a user query using the RAG system.
    
    Args:
        query: Query object containing the users input.
    
    Returns:
        Response: Generated response with sources and processing metadata.
    
    Raises:
        HTTPException: For various error conditions with appropriate status codes.
    """
    try:
        return await handle_query(query)

    except ValueError as e:
        logger.warning(f"Invalid input: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        ) from e
    
    except asyncio.TimeoutError:
        logger.error("Query processing timed out")
        raise HTTPException(
            status_code=504,
            detail="Request timed out"
        )
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred while processing query"
        ) from e


@router.post("/ask",
            response_model=Response,
            include_in_schema=False)
async def ask(query: Query) -> Response:
    return RedirectResponse(url="/api/v1/process_query")