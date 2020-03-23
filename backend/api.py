import logging

import uvicorn
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
from elasticsearch import Elasticsearch
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from backend.config import DB_HOST, DB_USER, DB_PW, APM_SERVER
from backend.controller.errors.http_error import http_error_handler
from backend.controller.router import router as api_router
# from backend.events.fastapi import create_start_app_handler, create_stop_app_handler

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger(__name__)
logging.getLogger("elasticsearch").setLevel(logging.WARNING)

elasticsearch_client = Elasticsearch(
    hosts=[{"host": DB_HOST}], http_auth=(DB_USER, DB_PW), scheme="http", ca_certs=False, verify_certs=False
)


def get_application() -> FastAPI:
    application = FastAPI(title="Haystack API", debug=True, version="0.1")

    application.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
    )
    apm_config = {"SERVICE_NAME": "covid-backend", "SERVER_URL": APM_SERVER}
    elasticapm = make_apm_client(apm_config)
    application.add_middleware(ElasticAPM, client=elasticapm)

    application.add_exception_handler(HTTPException, http_error_handler)
    # application.add_event_handler("startup", create_start_app_handler(application))
    # application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.include_router(api_router)

    return application


app = get_application()

logger.info("Open http://127.0.0.1:8000/docs to see Swagger API Documentation.")
logger.info(
    """
Or just try it out directly: curl --request POST --url 'http://127.0.0.1:8000/models/1/faq-qa' --data '{"questions": ["What are symptoms?"]}'
"""
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
