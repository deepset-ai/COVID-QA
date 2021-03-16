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
# Recommendation for more efficiency
###############################################################################
# aggregate pattern can be applied to the following Python file
# Instead of having dictionary method for overall types, split the dictionary cetegory that applies to
# Search Bar and the NLP.
# The aggregate root of Search Bar takes feedback of irrelevant questions, relevant questions and questions
# that are not found on the server. 
# The aggregate root of NLP, on the other hand, takes feedbacks of wrong information, outdated inforamtion
# and questions that are not matchable with resources within NLP server. 
# By spliting the feedback category into two aggregate roots, it froms a small tree structure 
# which then also takes O(log n) rather than O(n) since it is no longer scheming through dictionary in array format
