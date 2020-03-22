from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
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
    if feedback_payload["feedback"] not in ("relevant", "fake", "outdated", "irrelevant"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Invalid 'feedback'. It must be one of relevant, fake, outdated or irrelevant",
        )
    feedback_payload["model_id"] = model_id
    api.elasticsearch_client.index(index=DB_INDEX_FEEDBACK, body=feedback_payload)
