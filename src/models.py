from pydantic import BaseModel
from typing import List


class SearchResult(BaseModel):
    document: str
    score: float
    snippet: str


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]