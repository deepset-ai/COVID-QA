from fastapi import FastAPI, HTTPException

import logging
from datetime import datetime

import os

from starlette.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)
logging.getLogger('elasticsearch').setLevel(logging.WARNING)

################# Config ##########################################


# DB
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "")
DB_PW = os.getenv("DB_PW", "")
DB_INDEX = os.getenv("DB_INDEX", "document")
ES_CONN_SCHEME = os.getenv("ES_CONN_SCHEME", "http")
TEXT_FIELD_NAME = os.getenv("TEXT_FIELD_NAME", "text")
SEARCH_FIELD_NAME = os.getenv("SEARCH_FIELD_NAME", "text")
EMBEDDING_FIELD_NAME = os.getenv("EMBEDDING_FIELD_NAME", None)
EMBEDDING_DIM = os.getenv("EMBEDDING_DIM", None)



################################################################
from covidbackend.events.fastapi import create_start_app_handler, create_stop_app_handler
from covidbackend.controller.router import router as api_router
from covidbackend.controller.errors.http_error import http_error_handler

def get_application() -> FastAPI:
    application = FastAPI(title="Haystack API", debug=True, version=0.1)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))


    application.include_router(api_router)

    return application


app = get_application()


logger.info("Open http://127.0.0.1:8000/docs to see Swagger API Documentation.")
logger.info("""
Or just try it out directly: curl --request POST --url 'http://127.0.0.1:8000/models/1/doc-qa' --data '{"questions": ["Who is the father of Arya Starck?"]}'
""")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
