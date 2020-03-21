from fastapi import APIRouter
from pydantic import BaseModel

from backend import api
from backend.config import DB_INDEX_FEEDBACK

router = APIRouter()


class Feedback(BaseModel):
    question: str
    answer: str
    feedback: str
    document_id: int


@router.post("/models/{model_id}/feedback")
def feedback(model_id: int, request: Feedback):
    feedback_payload = request.__dict__
    feedback_payload["model_id"] = model_id
    api.elasticsearch_client.index(index=DB_INDEX_FEEDBACK, body=feedback_payload)
