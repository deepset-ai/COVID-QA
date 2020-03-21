
from fastapi import FastAPI
import logging
import os

from haystack.database.elasticsearch import ElasticsearchDocumentStore

logger = logging.getLogger(__name__)


# DB
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "")
DB_PW = os.getenv("DB_PW", "")
DB_INDEX = os.getenv("DB_INDEX", "document")
#

#
#
async def connect_to_db(app: FastAPI) -> None:
#
#
    logger.info(f"[Elasticsearch] Try to connect to: DB_HOST={DB_HOST}, DB_USER={len(DB_USER)*'*'}, DB_PW={len(DB_PW)*'*'}, DB_INDEX={DB_INDEX}")

    # Todo connect here to elasticsearch and make it available also for other endpoints;
    logger.info("[Elasticsearch] Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    # required
    # app.state.document_store.close_db_connection()

    logger.info("Connection closed")
