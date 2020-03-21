
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel

router = APIRouter()

class Request(BaseModel):
    search: str

class SuggestionResponse(BaseModel):
    suggestions: List[str]


@router.get("/query/autocomplete")
def ask(request: Request):
    return {"results": []}

