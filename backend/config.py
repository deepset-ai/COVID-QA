import ast
import os

# Resources / Computation
USE_GPU = os.getenv("USE_GPU", "True").lower() == "true"
MAX_PROCESSES = int(os.getenv("MAX_PROCESSES", 4))
BATCHSIZE = int(os.getenv("BATCHSIZE", 50))

# Monitoring
APM_SERVER = "http://localhost:8200"

# Reader
READER_MODEL_PATH = os.getenv("READER_MODEL_PATH", None)
CONTEXT_WINDOW_SIZE = int(os.getenv("CONTEXT_WINDOW_SIZE", 500))
DEFAULT_TOP_K_READER = int(os.getenv("DEFAULT_TOP_K_READER", 5))
TOP_K_PER_CANDIDATE = int(os.getenv("TOP_K_PER_CANDIDATE", 3))
NO_ANS_BOOST = int(os.getenv("NO_ANS_BOOST", -10))
DOC_STRIDE = int(os.getenv("DOC_STRIDE", 128))
MAX_SEQ_LEN = int(os.getenv("MAX_SEQ_LEN", 256))

# Retriever
DEFAULT_TOP_K_RETRIEVER = int(os.getenv("DEFAULT_TOP_K_RETRIEVER", 10))
EMBEDDING_MODEL_PATH = os.getenv("EMBEDDING_MODEL_PATH", "deepset/sentence_bert")
EMBEDDING_POOLING_STRATEGY = os.getenv("EMBEDDING_POOLING_STRATEGY", "reduce_mean")
EMBEDDING_EXTRACTION_LAYER = int(os.getenv("EMBEDDING_EXTRACTION_LAYER", -2))

# Database access
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "")
DB_PW = os.getenv("DB_PW", "")
DB_INDEX = os.getenv("DB_INDEX", "document")
DB_INDEX_FEEDBACK = os.getenv("DB_INDEX_FEEDBACK", "feedback")
ES_CONN_SCHEME = os.getenv("ES_CONN_SCHEME", "http")
TEXT_FIELD_NAME = os.getenv("TEXT_FIELD_NAME", "answer")
SEARCH_FIELD_NAME = os.getenv("SEARCH_FIELD_NAME", "question")
EMBEDDING_FIELD_NAME = os.getenv("EMBEDDING_FIELD_NAME", "question_emb")
EMBEDDING_DIM = os.getenv("EMBEDDING_DIM", None)

EXCLUDE_META_DATA_FIELDS = os.getenv("EXCLUDE_META_DATA_FIELDS", "['question_emb']")
if EXCLUDE_META_DATA_FIELDS:
    EXCLUDE_META_DATA_FIELDS = ast.literal_eval(EXCLUDE_META_DATA_FIELDS)

# SIL language detection API
SIL_API_KEY=os.getenv("SIL_API_KEY", "")
SIL_API_SECRET=os.getenv("SIL_API_SECRET", "")
SIL_API_URL=os.getenv("SIL_API_URL", "https://langdetect.apis.sil.org/langdetect")
