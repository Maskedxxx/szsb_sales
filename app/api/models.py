# models.py
from typing import List
from pydantic import BaseModel

class Subsector(BaseModel):
    id: str
    name: str

class Query(BaseModel):
    question: str
    subsectorId: str

class Metadata(BaseModel):
    selected_keys: List[str]
    selected_files: List[str]
    app_version: str
    key_selection_model: str
    rerank_model: str
    generation_model: str

class Response(BaseModel):
    answer: str
    meta: Metadata
