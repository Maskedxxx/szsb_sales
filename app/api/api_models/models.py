# app/api/models/models.py

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class Subsector(BaseModel):
    """Model representing a production subsector"""
    id: str = Field(..., description="Unique identifier for the subsector")
    name: str = Field(..., description="Name of the subsector")
    description: Optional[str] = Field(None, description="Optional description of the subsector")

    @field_validator('id')
    def validate_id(cls, v):
        if not v.strip():
            raise ValueError("ID cannot be empty")
        return v

class Query(BaseModel):
    """Model representing a user query"""
    question: str = Field(..., min_length=1, max_length=1000, description="The query text to process")
    subsector_id: Optional[str] = Field(None, alias="subsector_id", description="Subsector ID to scope the search")

    model_config = {
        "populate_by_name": True  # Allows using both alias and field names
    }


class Metadata(BaseModel):
    """Model representing metadata about the response generation process"""
    selected_keys: List[str] = Field(
        description="Route keys selected for the response",
        examples=[["stabilizers_and_thickeners"]]
    )
    selected_files: List[str] = Field(
        description="Source documents used for response generation",
        examples=[["meat/conservants_stabilizers_and_thickeners_list.json"]]
    )
    app_version: str
    key_selection_model: str
    rerank_model: str
    generation_model: str

class Response(BaseModel):
    answer: str = Field(..., description="Generated response to the query")
    meta: Metadata
