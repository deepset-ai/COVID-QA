from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from backend import api
from backend.config import DB_INDEX_FEEDBACK

router = APIRouter()


class Feedback(BaseModel):
    # Note: the question here is the user's question (=query) and not the matched one from our FAQs (=response)
    question: str
    answer: Optional[str]
    feedback: str
    document_id: int


@router.post("/models/{model_id}/feedback")
def feedback(model_id: int, request: Feedback):
    if not isValid(request):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Invalid 'feedback'. It must be one of relevant, fake, outdated or irrelevant",
        )
    request.__dict__["model_id"] = model_id
    api.elasticsearch_client.index(index=DB_INDEX_FEEDBACK, body=request.__dict__)

    
def isValid(request: Feedback):
    if request.__dict__["feedback"] not in ("relevant", "fake", "outdated", "irrelevant"):
        return False
    else:
        return True
