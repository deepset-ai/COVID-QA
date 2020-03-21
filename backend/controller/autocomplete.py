from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Request(BaseModel):
    search: str


class SuggestionResponse(BaseModel):
    suggestions: List[str]


@router.get("/query/autocomplete")
def ask(request: Request):
    return {"results": []}
