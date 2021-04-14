from preprocess import Preprocessor
from tfidf_train import TfidfTrainer
from tfidf_client import TfidfEvaluator

class LeafElement:
    def __init__(self, *args):
        self.position = args[0]

        def detail(self):
            print(self.position)


class CompositeElement:
    def __init__(self):
        self.child = []
    
    def add(self, child):
        self.children.append(child)
    
    def remove(self, child):
        self.children.remove(child)

    def detail(self):
        print(self.position)
        for child in self.children:
            child.detail()
