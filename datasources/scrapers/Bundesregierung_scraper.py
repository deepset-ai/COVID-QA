from datetime import date

import scrapy


class CovidScraper(scrapy.Spider):
    name = "Bundesregierung_scraper"
    start_urls = ["https://www.bundesregierung.de/breg-de/themen/coronavirus/ausbreitung-coronavirus-1716188"]

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

        QUESTION_ELEMENT_SELECTOR = "h2.mt-3"
        QUESTION_SELECTOR = "::text"

        questions = response.css(QUESTION_ELEMENT_SELECTOR)
        for question_elm in questions:
            question = question_elm.css(QUESTION_SELECTOR).getall()
            question = " ".join(question).strip()

            # all paragraphs till the next question header are considert to be the answer
            following_siblings = question_elm.xpath('following-sibling::*')
            answer = []
            answer_html = []
            for elm in following_siblings:
                if elm.root.tag == 'p' and 'navToTop' not in elm.root.classes:
                    answer += elm.css("::text").getall()
                    answer_html += [elm.get()]
                else:
                    break
            answer = "".join(answer).replace('\n', '').strip()
            answer_html = " ".join(answer_html).strip()

            # add question-answer pair to data dictionary
            columns["question"].append(question)
            columns["answer"].append(answer)
            columns["answer_html"].append(answer_html)

        today = date.today()

        columns["link"] = [
                              "https://www.bundesregierung.de/breg-de/themen/coronavirus/ausbreitung-coronavirus-1716188"] * len(
            columns["question"])
        columns["name"] = ["Wichtige Fragen und Antworten zum Coronavirus"] * len(columns["question"])
        columns["source"] = ["Presse- und Informationsamt der Bundesregierung"] * len(columns["question"])
        columns["category"] = [""] * len(columns["question"])
        columns["country"] = ["DE"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["de"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns
