from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from backend import api
from backend.config import DB_INDEX_FEEDBACK

import copy

router = APIRouter()


class Feedback(BaseModel):
    # Note: the question here is the user's question (=query) and not the matched one from our FAQs (=response)
    question: str
    answer: Optional[str]
    feedback: str
    document_id: int


class FeedbackCopier:
    def _init_(self):
        self.question = Feedback.question
        self.answer = Feedback.answer
        self.feedback = Feedback.eedback
        self.document_id = Feedback.document_id

    def clone(self):
        return type(self)(
            copy.deepcopy(self.question),
            copy.deepcopy(self.answer),
            copy.deepcopy(self.feedback),
            copy.deepcopy(self.document_id)
        )


@router.post("/models/{model_id}/feedback")
def feedback(model_id: int, request: Feedback):
    feedback_payload = request._dict_
    if feedback_payload["feedback"] not in ("relevant", "fake", "outdated", "irrelevant"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Invalid 'feedback'. It must be one of relevant, fake, outdated or irrelevant",
        )
    feedback_payload["model_id"] = model_id
    api.elasticsearch_client.index(index=DB_INDEX_FEEDBACK, body=feedback_payload)
