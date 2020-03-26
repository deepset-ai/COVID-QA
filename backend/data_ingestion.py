import pandas as pd
from haystack import Finder
from haystack.database.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.elasticsearch import ElasticsearchRetriever

def index_new_docs(document_store, retriever):
    # Get dataframe with questions, answers and some metadata
    df = pd.read_csv("data/faqs/faq_covidbert.csv")
    df.fillna(value="", inplace=True)

    # Index to ES
    if document_store.get_document_count() == 0:
        docs_to_index = []
        for idx, row in df.iterrows():
            d = row.to_dict()
            d = {k: v.strip() for k, v in d.items()}
            d["document_id"] = idx
            # add embedding
            question_embedding = retriever.create_embedding(row["question"])
            d["question_emb"] = question_embedding
            docs_to_index.append(d)
            print(idx)
        document_store.write_documents(docs_to_index)


def update_embeddings(document_store, retriever):
    #TODO move this upstream into haystack
    body = {
        "size": 10000,
        "query": {
        "match_all": {}
    },
    "_source": {"includes":["question"]}

}
    results = document_store.client.search(index=document_store.index, body=body, )["hits"]["hits"]
    # update embedding field
    for r in results:
        question_embedding = retriever.create_embedding(r["_source"]["question"])

        body = {
        "doc" : {
            "question_emb": question_embedding
        }
    }
        document_store.client.update(index=document_store.index, id=r["_id"], body=body)


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

    MODEL = "deepset/sentence_bert"
    GPU = False

    retriever = ElasticsearchRetriever(document_store=document_store, embedding_model=MODEL, gpu=GPU,
                                       emb_extraction_layer=-2, pooling_strategy="reduce_mean")

    # index new docs
    index_new_docs(document_store, retriever)

    # or just update embeddings
    # update_embeddings(document_store, retriever)

    # test with a query
    finder = Finder(reader=None, retriever=retriever)
    prediction = finder.get_answers_via_similar_questions(question="How high is mortality?", top_k_retriever=10)
    for p in prediction["answers"]:
        print(p["question"])
