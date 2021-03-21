from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

import langid
langid.set_languages(['de', 'en'])  # ISO 639-1 codes

#
# not a good idea to work with global variables like this.
#
from backend import api


class Request(BaseModel):
    search: str


class Question:
    #Aggregate root
    def __init__(self, question: str, search: str):
        self.DB_INDEX_AUTOCOMPLETE = "autocomplete"
        self.router = APIRouter()
        self.question = question
        self.search = search

    def addQuestionToAutocomplete(question: str):
        # todo: if it already exists; we need to increment count;
        body = {
            'phrase': question,
            'count' : 1
        }
        res = api.elasticsearch_client.index(index=self.DB_INDEX_AUTOCOMPLETE,body=body)


    @self.router.get("/query/autocomplete")
    def ask(search: str):
        interim = api.elasticsearch_client.search(index=self.DB_INDEX_AUTOCOMPLETE, body=
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


        lang, score = langid.classify(search)

        return {
                "results":result,
                "language": lang
        }
