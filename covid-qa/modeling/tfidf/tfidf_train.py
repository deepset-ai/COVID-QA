# -*- coding: utf-8 -*-
import sys
import re
import pickle
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import Preprocessor

class TfidfTrainer():

    def __init__(self, instream = None):
        self.preprocessor = Preprocessor(instream = instream)
        self.feature_vectors = None
        self.vectorizer = None

    def preprocess_corpus(self, corpus = None):
        if corpus:
            pcorpus = self.preprocessor.preprocess_sp(corpus)
        else:
            pcorpus = self.preprocessor.sentencepiece_apply(self.preprocessor.corpus)
        return pcorpus

    def train_model(self, corpus):
        # creating vocabulary using uni-gram and bi-gram
        self.vectorizer = TfidfVectorizer(min_df=2, max_df=.95, ngram_range=(1, 2))
        self.vectorizer.fit(corpus) # fit the vectorizer with the list of texts
        self.feature_vectors = self.vectorizer.transform(corpus) # list of tfidf vectors

    def save_model(self, prefix = "./tfidf_"):
        with open(f"{prefix}feature_vectors.pkl", 'wb') as outfile:
            pickle.dump(self.feature_vectors, outfile)

        with open(f"{prefix}vectorizer.pkl", 'wb') as outfile:
            pickle.dump(self.vectorizer, outfile)

    def load_model(self, prefix = "./tfidf_"):
        with open(f"{prefix}feature_vectors.pkl", 'rb') as infile:
            self.feature_vectors = pickle.load(infile)

        with open(f"{prefix}vectorizer.pkl", 'rb') as infile:
            self.vectorizer = pickle.load(infile)


def main():
    trainer = TfidfTrainer()
    corpus = trainer.preprocess_corpus()
    trainer.train_model(corpus)
    trainer.save_model()
 
if __name__ == "__main__":
    main()
