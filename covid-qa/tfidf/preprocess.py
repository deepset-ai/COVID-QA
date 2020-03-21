import sys
import re
import os

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
import string

import sentencepiece as spm

class Preprocessor():

    def __init__(self, language = 'german', instream = None):
        self.language = language
        if instream:
            self.corpus_orig = self.read_string(instream)
        else:
            self.corpus_orig = self.read_articles(sys.stdin)
        self.corpus = self.preprocess(self.corpus_orig)

    def preprocess(self, corpus_list):
        preproc_corpus_list = []
        stopset = stopwords.words(self.language) + list(string.punctuation)
        for corpus in corpus_list:
            corpus = corpus.lower()
            corpus = " ".join([ i for i in word_tokenize(corpus) if i not in stopset ])
            preproc_corpus_list.append(corpus)
        return preproc_corpus_list

    def sentencepiece_train(self, corpus_list):
        fp_out = open("./sp_corpus.txt", 'w')
        for corpus in corpus_list:
            print(corpus, file=fp_out)
        fp_out.close()
        spm.SentencePieceTrainer.Train('--input=sp_corpus.txt --model_prefix=sp_model --vocab_size=24000 --max_sentence_length=10000 --character_coverage=1.0 --num_threads=4 --hard_vocab_limit=false')
        return None

    def sentencepiece_apply(self, corpus_list):
        sent_corpus_list = []
        sp = spm.SentencePieceProcessor()
        sp.Load("./sp_model.model")
        for corpus in corpus_list:
            sent_corpus_list.append(" ".join(sp.EncodeAsPieces(corpus)))
        return sent_corpus_list

    def read_articles(self, fp):
        articles = []
        for line in fp:
            if line.strip() != "":
                articles.append(line.strip())
        return articles

    def read_string(self, mystring):
        articles = [mystring]
        return articles

if __name__ == "__main__":
    preprocessor = Preprocessor(language = 'english')
    preprocessor.sentencepiece_train(preprocessor.corpus)
