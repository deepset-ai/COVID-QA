from datetime import date

import scrapy
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = "BAUA_scraper"
    start_urls = ["https://www.baua.de/DE/Themen/Arbeitsgestaltung-im-Betrieb/Biostoffe/FAQ/FAQ_node.html"]

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
        QUESTIONS_SELECTOR = "//div[@class='tabs-container']/h2[@class='heading']"
        QUESTION_SELECTOR = " ::text"
        ANSWERS_SELECTOR = "//div[@class='tabs-container']/div"
        ANSWER_SELECTOR = "*::text"
        ANSWER_HTML_SELECTOR = "*"

        for q in response.xpath(QUESTIONS_SELECTOR):
            question = q.css(QUESTION_SELECTOR).getall()
            question = " ".join(question).strip()

            columns["question"].append(question)

        for a in response.xpath(ANSWERS_SELECTOR):
            answer = a.css(ANSWER_SELECTOR).getall()
            answer = " ".join(answer).strip()
            answer_html = a.css(ANSWER_HTML_SELECTOR).getall()
            answer_html = " ".join(answer_html).strip()

            columns["answer"].append(answer)
            columns["answer_html"].append(answer_html)

        today = date.today()

        columns["link"] = [
                              "https://www.baua.de/DE/Themen/Arbeitsgestaltung-im-Betrieb/Biostoffe/FAQ/FAQ_node.html"] * len(
            columns["question"])
        columns["name"] = ["Antworten auf häufig gestellte Fragen zu beruflichen Tätigkeiten mit SARS-CoV-2"] * len(
            columns["question"])
        columns["source"] = ["Bundesanstalt für Arbeitsschutz und Arbeitsmedizin (BAuA)"] * len(columns["question"])
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
