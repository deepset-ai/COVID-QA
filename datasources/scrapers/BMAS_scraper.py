from datetime import date

import scrapy
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = "BMAS_scraper"
    start_urls = ["https://www.bmas.de/DE/Presse/Meldungen/2020/corona-virus-arbeitsrechtliche-auswirkungen.html"]

    def parse(self, response):
        columns = {
            "question": [],
            "answer": [],
            "answer_html": [],
            "link": [],
            "name": [],
            "source": [],
            "category": [],
            "country": [],
            "region": [],
            "city": [],
            "lang": [],
            "last_update": [],
        }

        QUESTION_ANSWER_SELECTOR = ".panel"
        QUESTION_SELECTOR = ".collapsed ::text"
        ANSWER_SELECTOR = "./div[@id[starts-with(., 'collapse')]]"

        questions_answers = response.css(QUESTION_ANSWER_SELECTOR)
        for question_answer in questions_answers:
            question = question_answer.css(QUESTION_SELECTOR).getall()
            question = " ".join(question).strip().replace("\xad", "")
            answer = question_answer.xpath(ANSWER_SELECTOR).css(" ::text").getall()
            answer = " ".join(answer).strip().replace("\xad", "")
            answer_html = question_answer.xpath(ANSWER_SELECTOR).get()

            # add question-answer pair to data dictionary
            columns["question"].append(question)
            columns["answer"].append(answer)
            columns["answer_html"].append(answer_html)

        today = date.today()

        columns["link"] = ["https://www.bmas.de/DE/Presse/Meldungen/2020/corona-virus-arbeitsrechtliche-auswirkungen.html"] * len(columns["question"])
        columns["name"] = ["Arbeits- und arbeitsschutzrechtliche Fragen zum Coronavirus (SARS-CoV-2)"] * len(columns["question"])
        columns["source"] = ["Bundesministerium für Arbeit und Soziales (BMAS)"] * len(columns["question"])
        columns["category"] = [""] * len(columns["question"])
        columns["country"] = ["DE"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["de"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(CovidScraper)
    process.start()
