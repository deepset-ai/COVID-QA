import pandas as pd
import numpy as np

from sklearn.metrics import roc_auc_score
from farm.utils import MLFlowLogger
from haystack.retriever.elasticsearch import ElasticsearchRetriever
from sklearn.metrics.pairwise import cosine_similarity
from covid_nlp.eval import eval_question_similarity

def eval_pretrained_transformers(eval_file, lang, models, pooling_methods, extraction_layers):
    for model_name in models:
        for pooling_method in pooling_methods:
            for extraction_layer in extraction_layers:
                experiment_name = model_name
                log_to_mlflow = True
                params = {"pooling_method": pooling_method,
                          "extraction_layer": extraction_layer}

                # load eval data
                df = pd.read_csv(eval_file)
                # predict similarity of samples (e.g. via embeddings + cosine similarity)
                # here: dummy preds for naive baseline
                y_true = df["similar"].values
                retriever = ElasticsearchRetriever(document_store=None, embedding_model=model_name, gpu=True)
                questions_1 = [{"text": v} for k, v in df["question_1"].to_dict().items()]
                questions_2 = [{"text": v} for k, v in df["question_2"].to_dict().items()]

                res1 = retriever.embedding_model.extract_vectors(dicts=questions_1,
                                                          extraction_strategy=params["pooling_method"],
                                                          extraction_layer=params["extraction_layer"])

                res2 = retriever.embedding_model.extract_vectors(dicts=questions_2,
                                                          extraction_strategy=params["pooling_method"],
                                                          extraction_layer=params["extraction_layer"])
                res1 = np.array([i["vec"] for i in res1])
                res2 = np.array([i["vec"] for i in res2])

                df["pred"] = np.diag(cosine_similarity(res1, res2))

                # eval & track results
                eval_question_similarity(y_true=y_true, y_pred=df["pred"].values, lang=lang, model_name=model_name,
                                         params=params, user="malte", log_to_mlflow=log_to_mlflow, run_name=experiment_name)

if __name__ == "__main__":
    eval_file =  "../data/eval_question_similarity_en.csv"
    lang = "en"
#    models = ["deepset/sentence_bert","bert-base-uncased", "DeepPavlov/bert-base-multilingual-cased-sentence"]
    models = ["deepset/quora_dedup_bert_base"]
    pooling_methods = ["reduce_mean","cls_token","reduce_max"]
    extraction_layers = [-1, -2]
    eval_pretrained_transformers(eval_file, lang, models, pooling_methods, extraction_layers)
