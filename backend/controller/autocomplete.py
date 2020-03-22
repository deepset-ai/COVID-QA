from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from backend import api
from backend.config import DB_INDEX_AUTOCOMPLETE

router = APIRouter()


class Request(BaseModel):
    search: str


class SuggestionResponse(BaseModel):
    suggestions: List[str]


@router.get("/models/{model_id}/faq-qa")
def ask(request: Request):
	result = []
	interim = api.elasticsearch_client.search(index=DB_INDEX_AUTOCOMPLETE, body=
	{
		'_source':['phrase'],
		'query':{
			'match':{"phrase":request}	
		},
		'sort' :[
			{'count' : {'order' : 'desc'}}
		]
	})
	if len(interim['hits']['hits']) < 10:
		for i in range(len(interim['hits']['hits'])):
			result.append(interim['hits']['hits'][i]['_source']['phrase'])
	else:
		for i in range(10):
			result.append(interim['hits']['hits'][i]['_source']['phrase'])
	return {"results":result}
