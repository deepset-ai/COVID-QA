from datetime import date

import scrapy


class CovidScraper(scrapy.Spider):
    name = "BMG_scraper"
    start_urls = ["https://www.zusammengegencorona.de/informieren/basiswissen-coronavirus/",
                  "https://www.zusammengegencorona.de/informieren/basiswissen-uebertragung/",
                  "https://www.zusammengegencorona.de/informieren/informationen-zum-test/",
                  "https://www.zusammengegencorona.de/informieren/symptome-erkennen/",
                  "https://www.zusammengegencorona.de/informieren/praevention/",
                  "https://www.zusammengegencorona.de/informieren/informationen-alltag/",
                  "https://www.zusammengegencorona.de/informieren/informationen-aeltere-menschen/",
                  "https://www.zusammengegencorona.de/informieren/medizinisches-personal/",
                  "https://www.zusammengegencorona.de/informieren/arbeitsschutz/",
                  "https://www.zusammengegencorona.de/informieren/wirtschaftliche-folgen/",
                  # not real answers, only links...
                  "https://www.zusammengegencorona.de/informieren/weitere-informationen/",
                  # very specific questions and answers as well as other links
                  "https://www.zusammengegencorona.de/informieren/zuhause-bleiben/"]

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

        QUESTION_ANSWER_SELECTOR = ".accordion__item"
        QUESTION_SELECTOR = ".accordion__heading ::text"
        ANSWER_SELECTOR = ".panel-inner ::text"
        ANSWER_HTML_SELECTOR = ".panel-inner"

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
            columns["link"].append(response.url)

        today = date.today()

        columns["name"] = ["Ihre Fragen - unsere Antworten zum neuartigen Coronavirus / COVID-19"] * len(
            columns["question"])
        columns["source"] = ["Bundesministerium für Gesundheit (BMG)"] * len(columns["question"])
        columns["category"] = [""] * len(columns["question"])
        columns["country"] = ["DE"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["de"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns
