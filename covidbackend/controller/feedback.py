
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel

router = APIRouter()

class Request(BaseModel):
    question: str

@router.post("/feedback")
def ask(request: Request):
    return {"results": []}

