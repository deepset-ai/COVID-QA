# run 'scrapy runspider WHO_scraper.py' to scrape data

from datetime import date
import scrapy
import pandas as pd


class WHOScraper(scrapy.Spider):
  name = "WHO_scraper"
  start_urls = ["https://www.who.int/news-room/q-a-detail/q-a-coronaviruses"]

  def parse(self, response):
    columns = {
      "question" : [],
      "answer" : [],
      "answer_html" : [],
      "link" : [],
      "name" : [],
      "source" : [],
      "category" : [],
      "country" : [],
      "region" : [],
      "city" : [],
      "lang" : [],
      "last_update" : [],
    }

    QUESTION_ANSWER_SELECTOR = ".sf-accordion__panel"
    QUESTION_SELECTOR = ".sf-accordion__link::text"
    ANSWER_SELECTOR = ".sf-accordion__content ::text"
    ANSWER_HTML_SELECTOR = ".sf-accordion__content"

    questions_answers = response.css(QUESTION_ANSWER_SELECTOR)
    for question_answer in questions_answers:
      question = question_answer.css(QUESTION_SELECTOR).getall()
      question = " ".join(question).strip()
      answer = question_answer.css(ANSWER_SELECTOR).getall()
      answer = " ".join(answer).strip()
      answer_html = question_answer.css(ANSWER_HTML_SELECTOR).getall()
      answer_html = " ".join(answer_html).strip()

      # add question-answer pair to data dictionary
      columns["question"].append(question)
      columns["answer"].append(answer)
      columns["answer_html"].append(answer_html)

    today = date.today()

    columns["link"] = ["https://www.who.int/news-room/q-a-detail/q-a-coronaviruses"] * len(columns["question"])
    columns["name"] = ["Q&A on coronaviruses (COVID-19)"] * len(columns["question"])
    columns["source"] = ["World Health Organization (WHO)"] * len(columns["question"])
    columns["category"] = [""] * len(columns["question"])
    columns["country"] = [""] * len(columns["question"])
    columns["region"] = [""] * len(columns["question"])
    columns["city"] = [""] * len(columns["question"])
    columns["lang"] = ["en"] * len(columns["question"])
    columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

    dataframe = pd.DataFrame(columns)

    dataframe.to_csv("who.tsv", sep="\t", index=False)
 


