from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

import langid
langid.set_languages(['de', 'en'])  # ISO 639-1 codes

#
# not a good idea to work with global variables like this.
#
from backend import api

DB_INDEX_AUTOCOMPLETE = "autocomplete"

router = APIRouter()


class Request(BaseModel):
    search: str


def addQuestionToAutocomplete(question: str):
    # todo: if it already exists; we need to increment count;
    res = api.elasticsearch_client.index(index=DB_INDEX_AUTOCOMPLETE,body=AutoCompleteBody.add(question))




@router.get("/query/autocomplete")
def ask(search: str):
    interim = api.elasticsearch_client.search(index=DB_INDEX_AUTOCOMPLETE, body=AutoCompleteBody(search).ask)
    resultCount = len(interim['hits']['hits'])
    result = []
    for i in range(resultCount):
        result.append(interim['hits']['hits'][i]['_source']['phrase'])


    lang, score = langid.classify(search)

    return {
            "results":result,
            "language": lang
        }


