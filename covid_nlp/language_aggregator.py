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

	def add_question(self, data: dict):
		self._data[self._format_key(data["question"])] = Question(**data)

	def get_question(self, question: str) -> Union[None, Question]:
		return self._data.get(self._format_key(question))

	def _format_key(self, name: str) -> str:
		return name.lower().strip().strip("?.,/-_")


class LangAggregator:
	def __init__(self):
		self._data = {}
		with open("../data/faqs/faq_covidbert.csv", "r") as fp:
			reader = csv.DictReader(fp)
			# Skip the headers
			next(reader)
			for item in reader:
				if item["lang"] not in self._data:
					self._data[item["lang"]] = QuestionAggregator()
				self._data[item["lang"]].add_question(item)

	def get_lang(self, lang: str) -> Union[None, QuestionAggregator]:
		return self._data.get(lang)


if __name__ == "__main__":
	lang_aggregator = LangAggregator()
	print(lang_aggregator.get_lang("en").get_question("How is COVID-19 treated").answer)
