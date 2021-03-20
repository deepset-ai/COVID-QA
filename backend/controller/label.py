from typing import List


class Labels():
    answers: List[Label]


class Label():
    id: int
    questionText: str
    answer: str
    documentId: int

    def Label(questionText, answer, documentId):
        self.questionText = questionText
        self.answer = answer
        self.documentId = documentId
