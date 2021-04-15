from fastapi import APIRouter
router = APIRouter()

class AutoCompleteBody():
    input: str

def add(input: str):
    return ({'phrase': input,
        'count' : 1
    })



@router.get("/query/autocomplete")
def ask(input: str):
    return(
        {
        '_source':['phrase'],
        'query':{
            "bool": {
                "must": [{
                    "match": {
                        "phrase": input
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
