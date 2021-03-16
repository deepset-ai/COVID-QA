from fastapi import APIRouter
from pydantic import BaseModel

#auto-complete suggestions for user
import langid
langid.set_languages(['de', 'en'])  # ISO 639-1 codes

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from backend import api
from backend.config import DB_INDEX_FEEDBACK

router = APIRouter()
from backend import api

DB_INDEX_AUTOCOMPLETE = "autocomplete"

router = APIRouter()


class Request(BaseModel):
    search: str


def addQuestionToAutocomplete(question: str):
    # todo: if it already exists; we need to increment count;
    body = {
        'phrase': question,
        'count' : 1
    }
    res = api.elasticsearch_client.index(index=DB_INDEX_AUTOCOMPLETE,body=body)




@router.get("/query/autocomplete")
def ask(search: str):
    interim = api.elasticsearch_client.search(index=DB_INDEX_AUTOCOMPLETE, body=
    {
        '_source':['phrase'],
        'query':{
            "bool": {
                "must": [{
                    "match": {
                        "phrase": search
                    }
                },
                    {
                        "exists": {
                            "field": "count"
                        }
                    }]
            }
        },
        'size': 10,
        'sort' :[
                {'count' : {'order' : 'desc' }}
        ]
    })

    resultCount = len(interim['hits']['hits'])
    result = []
    #loop invariant result is not empty
    for i in range(resultCount):
        result.append(interim['hits']['hits'][i]['_source']['phrase'])
        len(result) != 0;


    lang, score = langid.classify(search)

    return {
            "results":result,
            "language": lang
        }

#feedback to give back to user

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