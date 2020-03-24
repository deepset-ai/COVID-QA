# run 'scrapy runspider ZEIT_scraper.py' to scrape data

from datetime import date
import scrapy

class CovidScraper(scrapy.Spider):
  name = "ZEIT_faq_scraper"
  start_urls = ["https://www.zeit.de/wissen/gesundheit/2020-02/coronavirus-sars-cov-2-risiko-symptome-schutz-rechte-faq"]

  custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    }

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

    QUESTION_ANSWER_SELECTOR = "div.article-page div[itemscope]:not(div[itemprop='acceptedAnswer'])"
    QUESTION_SELECTOR = ".article__subheading::text"
    ANSWER_SELECTOR = "p.paragraph.article__item ::text"
    ANSWER_HTML_SELECTOR = "p.paragraph.article__item"
    QUESTION_LINK_ID_SELECTOR = ".article__subheading"

    questions_answers = response.css(QUESTION_ANSWER_SELECTOR)
    for question_answer in questions_answers:
      question = question_answer.css(QUESTION_SELECTOR).getall()
      question = " ".join(question).strip()
      answer = question_answer.css(ANSWER_SELECTOR).getall()
      answer = " ".join(answer).replace('\n', '').replace('\xa0', '').strip()
      answer_html = question_answer.css(ANSWER_HTML_SELECTOR).getall()
      answer_html = " ".join(answer_html).strip()
      link_id = question_answer.css(QUESTION_LINK_ID_SELECTOR)[0].root.attrib['id']

      # add question-answer pair to data dictionary
      columns["question"].append(question)
      columns["answer"].append(answer)
      columns["answer_html"].append(answer_html)
      columns["link"].append("https://www.zeit.de/wissen/gesundheit/2020-02/coronavirus-sars-cov-2-risiko-symptome-schutz-rechte-faq#" + link_id)

    today = date.today()

    columns["name"] = ["Coronavirus Sars-CoV-2: Die wichtigsten Antworten zum Corona-Ausbruch"] * len(columns["question"])
    columns["source"] = ["ZEIT ONLINE GmbH"] * len(columns["question"])
    columns["category"] = [""] * len(columns["question"])
    columns["country"] = [""] * len(columns["question"])
    columns["region"] = [""] * len(columns["question"])
    columns["city"] = [""] * len(columns["question"])
    columns["lang"] = ["de"] * len(columns["question"])
    columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

    return columns
 


