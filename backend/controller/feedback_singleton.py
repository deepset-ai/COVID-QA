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
    feedback_payload = request.__dict__
    if feedback_payload["feedback"] not in ("relevant", "fake", "outdated", "irrelevant"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Invalid 'feedback'. It must be one of relevant, fake, outdated or irrelevant",
        )
    feedback_payload["model_id"] = model_id
    api.elasticsearch_client.index(index=DB_INDEX_FEEDBACK, body=feedback_payload)

###############################################################################
# Creational Design Pattern - Singleton is applied  on this file. 
###############################################################################
# Despite of different types in ase of reporting feedbacks, the file only holds one instance, "feedback", to 
# handle all types of feedbacks - revelant, fake, outdated and irrelevant. 
# There is nothing I need to adjust on this file because it already implements singleton design pattern.
# The purpose of the singleton design pattern is to ensure a class has only one instance,
# while providing a global point of access to it, whcih the function "feedback" already behaves. 
# The users only have accessibility on feedback since the feedback is the only instance that can be handled. 
# Moreover, feedback is infinitely repeateable with selecting different types of feedbacks. 
