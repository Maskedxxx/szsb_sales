# models.py
from typing import List
from pydantic import BaseModel

class Subsector(BaseModel):
    id: str
    name: str

class Query(BaseModel):
    question: str
    subsectorId: str

class Response(BaseModel):
    answer: str
    selected_files: List[str]
    selected_keys: List[str]