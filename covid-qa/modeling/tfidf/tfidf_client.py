import sys
import re
import pickle
import os
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd

from preprocess import Preprocessor
from tfidf_train import TfidfTrainer

sys.path.insert(0, "./../../")
from eval import eval_question_similarity


class TfidfEvaluator():
    def __init__(self):
        self.model = TfidfTrainer(instream = "dummy")
        self.model.load_model()

    def process_string(self, mystring):
        corpus = self.model.preprocess_corpus([mystring])
        corpus_vectors = self.model.vectorizer.transform([corpus[0]])
        return corpus_vectors

    def find_best_matches(self, cos_list, top_n = 10):
        cos_list_enumerated = [ (i, cos_sim) for i, cos_sim in enumerate(cos_list) ]
        cos_list_enumerated.sort(key=lambda x:x[1], reverse=True)
        return cos_list_enumerated[:top_n]

    def score_string_pair(self, string1, string2):
        vec1 = self.process_string(string1)
        vec2 = self.process_string(string2)
        cos_sim = cosine_similarity(vec1, vec2)
        return cos_sim[0][0]

def main():
    evaluator = TfidfEvaluator()

    eval_file = "../../../data/eval_question_similarity_en.csv"
    df = pd.read_csv(eval_file)
    # predict similarity of samples (e.g. via embeddings + cosine similarity)
    df['pred'] = df.apply(lambda x: evaluator.score_string_pair(x.question_1, x.question_2), axis=1)
    y_true = df["similar"].values
    y_pred = df["pred"].values

    model_name = "tfidf_baseline"
    exp_name = "tfidf_cos_sim_2"
    params = {"sp_voc": 16000, "max_ngram": 2, "remove_stopwords": 1, 
                "data_train": "eval, scraped", "data_sp": "eval, scraped, CORD-19.200k"}
    eval_question_similarity(y_true=y_true, y_pred=y_pred, lang="en", model_name=model_name,
                             params=params, user="carmen", log_to_mlflow=True, run_name=exp_name)


if __name__ == "__main__":
    main()
