from typing import List
import copy


class Document():
    id: int
    answers: List[Answer]
    questions: List[Question]
    version: int
    documentCopy: Document

    def Document(self):
        self.documentCopy = copy.deepcopy(self)

    def modifyQuestion(self, question, answer):
        n = len(question.question)
        m = len(answer.answer)
        if n == 0 or m == 0:
            raise Exception("Invalid Question or Answer Length")
        if question.color != answer.color:
            raise Exception("coloring doesn't match")

    def addQuestion(self, question, answer):
        # validate the integrity
        n = len(question.question)
        m = len(answer.answer)
        if n == 0 or m == 0:
            raise Exception("Invalid Question or Answer Length")
        if question.color != answer.color:
            raise Exception("coloring doesn't match")

    def update(self):
        version = version+1
        # write the updated QuestionAnswer into Database
        # create diff of self and documentCopy
        # and insert label for each item
        # update labels in database for each different question/answer

    class Answer():
        id: int
        documentId: int
        answer: str
        color: str
        position: Position

        class Position():
            start: int
            end: int

    class Question():
        id: int
        documentId: int
        question: str
        color: str
