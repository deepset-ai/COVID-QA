import logging
from datetime import datetime
from typing import List, Dict, Optional

import elasticapm
from fastapi import APIRouter
from fastapi import HTTPException
from haystack import Finder
from haystack.database.elasticsearch import ElasticsearchDocumentStore
from haystack.reader.farm import FARMReader
from haystack.retriever.elasticsearch import ElasticsearchRetriever
from pydantic import BaseModel

from backend.config import (
    DB_HOST,
    DB_USER,
    DB_PW,
    DB_INDEX,
    ES_CONN_SCHEME,
    TEXT_FIELD_NAME,
    SEARCH_FIELD_NAME,
    EMBEDDING_DIM,
    EMBEDDING_FIELD_NAME,
    EXCLUDE_META_DATA_FIELDS,
    EMBEDDING_MODEL_PATH,
    EMBEDDING_POOLING_STRATEGY,
    EMBEDDING_EXTRACTION_LAYER,
    READER_MODEL_PATH,
    BATCHSIZE,
    USE_GPU,
    CONTEXT_WINDOW_SIZE,
    TOP_K_PER_CANDIDATE,
    NO_ANS_BOOST,
    MAX_PROCESSES,
    MAX_SEQ_LEN,
    DOC_STRIDE,
    DEFAULT_TOP_K_READER,
    DEFAULT_TOP_K_RETRIEVER,
)
from backend.controller.autocomplete import addQuestionToAutocomplete

logger = logging.getLogger(__name__)


router = APIRouter()


document_store = ElasticsearchDocumentStore(
    host=DB_HOST,
    username=DB_USER,
    password=DB_PW,
    index=DB_INDEX,
    scheme=ES_CONN_SCHEME,
    ca_certs=False,
    verify_certs=False,
    text_field=TEXT_FIELD_NAME,
    search_fields=SEARCH_FIELD_NAME,
    embedding_dim=EMBEDDING_DIM,
    embedding_field=EMBEDDING_FIELD_NAME,
    excluded_meta_data=EXCLUDE_META_DATA_FIELDS,
)

# multilingual baseline retriever (=BM25)
retriever = ElasticsearchRetriever(document_store=document_store, embedding_model=None, gpu=USE_GPU)

# english_retriever
english_retriever = ElasticsearchRetriever(document_store=document_store, embedding_model=EMBEDDING_MODEL_PATH, gpu=USE_GPU,
                                   pooling_strategy=EMBEDDING_POOLING_STRATEGY, emb_extraction_layer=EMBEDDING_EXTRACTION_LAYER)


if READER_MODEL_PATH:
    # needed for extractive QA
    reader = FARMReader(
        model_name_or_path=str(READER_MODEL_PATH),
        batch_size=BATCHSIZE,
        use_gpu=USE_GPU,
        context_window_size=CONTEXT_WINDOW_SIZE,
        top_k_per_candidate=TOP_K_PER_CANDIDATE,
        no_ans_boost=NO_ANS_BOOST,
        max_processes=MAX_PROCESSES,
        max_seq_len=MAX_SEQ_LEN,
        doc_stride=DOC_STRIDE,
    )
else:
    # don't need one for pure FAQ matching
    reader = None

# TODO we should switch this later to use "en" / "de" etc in the endpoint than plain model ids
FINDERS = {1: Finder(reader=reader, retriever=retriever),
           2: Finder(reader=reader, retriever=english_retriever)}


#############################################
# Basic data schema for request & response
#############################################
class Query(BaseModel):
    questions: List[str]
    filters: Dict[str, Optional[str]] = None
    top_k_reader: int = DEFAULT_TOP_K_READER
    top_k_retriever: int = DEFAULT_TOP_K_RETRIEVER


class Answer(BaseModel):
    answer: Optional[str]
    question: Optional[str]
    score: float = None
    probability: float = None
    context: Optional[str]
    offset_start: int
    offset_end: int
    meta: Optional[Dict[str, Optional[str]]]
    # document_id: Optional[str] = None
    # document_name: Optional[str]
    # TODO move these two into "meta" also for the regular extractive QA


class ResponseToIndividualQuestion(BaseModel):
    question: str
    answers: List[Optional[Answer]]


class Response(BaseModel):
    results: List[ResponseToIndividualQuestion]


#############################################
# Endpoints
#############################################

# # CURL example: curl --request POST --url 'http://127.0.0.1:8000/models/1/doc-qa' --data '{"questions": ["Who is the father of Arya Starck?"]}
# @router.post("/models/{model_id}/doc-qa", response_model=Response, response_model_exclude_unset=True)
# def ask(model_id: int, request: Query):
#     finder = FINDERS.get(model_id, None)
#     if not finder:
#         raise HTTPException(
#             status_code=404, detail=f"Couldn't get Finder with ID {model_id}. Available IDs: {list(FINDERS.keys())}"
#         )
#
#     results = []
#     for question in request.questions:
#         if request.filters:
#             # put filter values into a list and remove filters with null value
#             request.filters = {key: [value] for key, value in request.filters.items() if value is not None}
#             logger.info(f" [{datetime.now()}] Request: {request}")
#
#         result = finder.get_answers(
#             question=question,
#             top_k_retriever=request.top_k_retriever,
#             top_k_reader=request.top_k_reader,
#             filters=request.filters,
#         )
#         results.append(result)
#
#         logger.info({"request": request.json(), "results": results})
#
#         # remember questions with result in the autocomplete
#         if len(results) > 0:
#             addQuestionToAutocomplete(question)
#
#         return {"results": results}

# CURL example: curl --request POST --url 'http://127.0.0.1:8000/question/ask' --data '{"questions": ["Who is the father of Arya Starck?"]}
@router.post("/question/ask", response_model=Response, response_model_exclude_unset=True)
def ask(request: Query):
    # todo provide some logic to determin the model, e.g. language, is it FAQ or QA etc.

    return askFaq(1, request)
    

@router.post("/models/{model_id}/faq-qa", response_model=Response, response_model_exclude_unset=True)
def ask_faq(model_id: int, request: Query):

    finder = FINDERS.get(model_id, None)
    if not finder:
        raise HTTPException(
            status_code=404, detail=f"Couldn't get Finder with ID {model_id}. Available IDs: {list(FINDERS.keys())}"
        )

    results = []
    for question in request.questions:
        if request.filters:
            # put filter values into a list and remove filters with null value
            request.filters = {key: [value] for key, value in request.filters.items() if value is not None}
            logger.info(f" [{datetime.now()}] Request: {request}")

        # temporary routing of requests by language
        result = finder.get_answers_via_similar_questions(
            question=question, top_k_retriever=request.top_k_retriever, filters=request.filters,
        )
        results.append(result)

        elasticapm.set_custom_context({"results": results})
        logger.info({"request": request.json(), "results": results})

        # remember questions with result in the autocomplete
        if len(results) > 0:
            addQuestionToAutocomplete(question)

        return {"results": results}
