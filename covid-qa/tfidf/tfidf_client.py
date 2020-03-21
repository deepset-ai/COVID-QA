import sys
import re
import pickle
import os
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import Preprocessor
from tfidf_train import TfidfTrainer


class TfidfEvaluator():
    def __init__(self):
        self.model = TfidfTrainer()
        self.model.load_model()

    def process_string(self):
        corpus = self.model.preprocess_corpus()
        c = corpus[0]
        corpus_vectors = self.model.vectorizer.transform([c])
        return corpus_vectors

    def find_best_matches(self, cos_list):
        cos_list_enumerated = [ (i, cos_sim) for i, cos_sim in enumerate(cos_list) ]
        #cos_list_filtered = [ x for x in cos_list_enumerated if x[1] < 0.95 ]
        cos_list_enumerated.sort(key=lambda x:x[1], reverse=True)
        return cos_list_enumerated[:10]

def main():
    evaluator = TfidfEvaluator()

    corpus_vectors = evaluator.process_string()
    cos_list = []
    cos_sim = cosine_similarity(corpus_vectors, evaluator.model.feature_vectors)
    best_art = evaluator.find_best_matches(cos_sim[0])
    print(best_art)

if __name__ == "__main__":
    main()
