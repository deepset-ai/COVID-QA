from typing import List


class Labels():
    answers: List[Label]


class Label():
    id: int
    questionText: str
    answer: str
    documentId: int
    creatorId: int

    def Label(self, questionText, answer, documentId, creatorId):
        self.questionText = questionText
        self.answer = answer
        self.documentId = documentId
        self.creatorId = creatorId
