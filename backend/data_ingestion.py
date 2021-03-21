import pandas as pd
from haystack import Finder
from haystack.database.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.elasticsearch import ElasticsearchRetriever


if __name__=="__main__":

    document_store = ElasticsearchDocumentStore(
        host="localhost",
        username="",
        password="",
        index="document",
        text_field="answer",
        embedding_field="question_emb",
        embedding_dim=768,
        excluded_meta_data=["question_emb"],
    )

    retriever = ElasticsearchRetriever(document_store=document_store, embedding_model=MODEL, gpu=GPU,
                                       emb_extraction_layer=-2, pooling_strategy="reduce_mean")

    Ingestion.update_document_store(document_store)
    Ingestion.update_retriever(retriever)

    # index new docs
    Ingestion.index(document_store, retriever)


class Ingestion:
    def __init__(self, document_store, retriever):
        self.document_store = document_store
        self.retriever = retriever
        self.MODEL = "deepset/sentence_bert"
        self.GPU = False

    def index_new_docs(document_store, retriever):
        update_document_store(document_store)
        update_retriever(retriever)
        # Get dataframe with questions, answers and some metadata
        df = pd.read_csv("data/faqs/faq_covidbert.csv")
        df.fillna(value="", inplace=True)

        # Index to ES
        if self.document_store.get_document_count() == 0:
            docs_to_index = []
            for idx, row in df.iterrows():
                d = row.to_dict()
                d = {k: v.strip() for k, v in d.items()}
                d["document_id"] = idx
                # add embedding
                question_embedding = self.retriever.create_embedding(row["question"])
                d["question_emb"] = question_embedding
                docs_to_index.append(d)
                print(idx)
            self.document_store.write_documents(docs_to_index)

    def update_embeddings(document_store, retriever):
        update_document_store(document_store)
        update_retriever(retriever)
        #TODO move this upstream into haystack
        body = {
            "size": 10000,
            "query": {
            "match_all": {}
        },
        "_source": {"includes":["question"]}
    }

        results = self.document_store.client.search(index=document_store.index, body=body, )["hits"]["hits"]
        # update embedding field
        for r in results:
            question_embedding = self.retriever.create_embedding(r["_source"]["question"])

            body = {
            "doc" : {
                "question_emb": question_embedding
            }
        }
            self.document_store.client.update(index=self.document_store.index, id=r["_id"], body=body)

    def index(document_store, retriever):
        index_new_docs(document_store, retriever)

    def update_document_store(document_store):
        self.document_store = document_store

    def update_retriever(retriever):
        self.retriever = retriever
