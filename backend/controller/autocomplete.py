from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

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
    for i in range(resultCount):
        result.append(interim['hits']['hits'][i]['_source']['phrase'])

    return {
            "results":result,
            "language": "en"
        }


