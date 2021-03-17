import csv

from dataclasses import dataclass
from typing import Union


@dataclass
class Question:
	question: str
	answer: str
	answer_html: str
	link: str
	name: str
	source: str
	category: str
	country: str
	region: str
	city: str
	lang: str
	last_update: str


class QuestionAggregator:
	def __init__(self):
		self._data = {}
		with open("../data/faqs/faq_covidbert.csv", "r") as fp:
			reader = csv.DictReader(fp)
			# Skip the headers
			next(reader)
			for item in reader:
				self._data[self._format_key(item["question"])] = Question(**item)

	def get_question(self, question: str) -> Union[None, Question]:
		return self._data.get(self._format_key(question))

	def _format_key(self, name: str) -> str:
		return name.lower().strip().strip("?.,/-_")


if __name__ == "__main__":
	question_aggregator = QuestionAggregator()
	print(question_aggregator.get_question("How is COVID-19 treated").answer)
