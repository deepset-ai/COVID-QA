from __future__ import annotations
from abc import ABC, abstractmethod
from preprocess import Preprocessor
from tfidf_train import TfidfTrainer
from tfidf_client import TfidfEvaluator
import sys
import pandas as pd
sys.path.insert(0, "./../../")
from eval import eval_question_similarity

# Context class to control the transition between various states and the initial state
# the state transition flow will be recorded and presented by Context class as well. 
class Context:
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.
    """

    # A reference to the current state of the Context.
    _state = None

    def getState(self) -> State:
        return self._state

    def setState(self, _state) -> None:
        self._state = _state

    # The Context delegates part of its behavior to the current State object.
    def preprocess(self):
        self.setState(self._state.preprocess())

    def train(self):
        self.setState(self._state.train())

    def evaluate(self):
        self.setState(self._state.evaluate())


# abstract state class
class State:

    @abstractmethod
    def preprocess(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass


# several concrete state classes, implement various behaviors, associate with a state of the Context.
class PreprocessState(State):
    def preprocess(self):
        print("preprossing language...")
        vocab_size = 24000
        if len(sys.argv) > 1:
            vocab_size = sys.argv[1]
        print("Create Preprocessor")
        preprocessor = Preprocessor(language = 'english')
        print("Train spm")
        preprocessor.sentencepiece_train(preprocessor.corpus, vocab_size = vocab_size)

    def train(self):
        print("Sorry you cannot do training now, please preprocess the language !")
        return self

    def evaluate(self):
        print("Sorry you cannot do evaluation now, please preprocess the language !")
        return self


class TrainState(State):
    def preprocess(self):
        print("Sorry language has been preprocessed, please do training !")
        return self

    def train(self):
        print("Training...")
        trainer = TfidfTrainer()
        corpus = trainer.preprocess_corpus()
        trainer.train_model(corpus)
        trainer.save_model()

    def evaluate(self):
        print("Sorry you cannot do evaluation now, please do training !")
        return self


class EvaluateState(State):
    def preprocess(self):
        print("Sorry language has been preprocessed, please do training !")
        return self

    def train(self):
        print("Sorry model has been trained, please do evaluation !")
        return self

    def evaluate(self):
        print("Evaluating...")
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

    # The client code of workflow process
    workflow = Context()
    workflow.setState(PreprocessState())
    workflow.preprocess()
    workflow.train()
    workflow.evaluate()