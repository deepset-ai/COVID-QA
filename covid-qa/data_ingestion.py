from haystack import Finder
from haystack.database.elasticsearch import ElasticsearchDocumentStore

from haystack.retriever.elasticsearch import ElasticsearchEmbeddingRetriever
from haystack.utils import print_answers
import pandas as pd

MODEL = "DeepPavlov/bert-base-multilingual-cased-sentence"
GPU = False

document_store = ElasticsearchDocumentStore(host="localhost", username="", password="",
                                            index="document", text_field="answer",
                                            embedding_field="question_emb",
                                            embedding_dim=768,
                                            excluded_meta_data=["question_emb"])

retriever = ElasticsearchEmbeddingRetriever(document_store=document_store, embedding_model=MODEL, gpu=GPU)

# Get dataframe with questions, answers and some metadata
df = pd.read_csv("data/faqs/faq_covidbert.csv")
df.fillna(value="", inplace=True)

# Index to ES
# if document_store.get_document_count() == 0:
if True:
    docs_to_index = []
    doc_id = 1
    for idx, row in df.iterrows():
        d = row.to_dict()
        d = {k:v.strip() for k, v in d.items()}
        d["document_id"] = idx
        # add embedding
        question_embedding = retriever.create_embedding(row["question"])
        d["question_emb"] = question_embedding
        docs_to_index.append(d)
        print(idx)
    document_store.write_documents(docs_to_index)


# Init reader & and use Finder to get answer
finder = Finder(reader=None, retriever=retriever)
prediction = finder.get_answers_via_similar_questions(question="How is the virus spreading?", top_k_retriever=10)
print_answers(prediction, details="all")
