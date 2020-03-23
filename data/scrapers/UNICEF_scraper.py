from datetime import date

import scrapy


class CovidScraper(scrapy.Spider):
    name = "UNICEF_scraper"
    start_urls = ["https://www.unicef.org/stories/novel-coronavirus-outbreak-what-parents-should-know"]

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

        QUESTION_ANSWER_SELECTOR = ".field .field--name-field-component-text-content"
        QUESTION_SELECTOR = "h4::text"
        ANSWER_SELECTOR = "p:not(p:contains('< Back')) ::text"
        ANSWER_HTML_SELECTOR = "p:not(p:contains('< Back'))"

        questions_answers = response.css(QUESTION_ANSWER_SELECTOR)
        for question_answer in questions_answers:
            question = question_answer.css(QUESTION_SELECTOR).getall()
            question = " ".join(question).strip()
            answer = question_answer.css(ANSWER_SELECTOR).getall()
            answer = " ".join(answer).strip()
            answer_html = question_answer.css(ANSWER_HTML_SELECTOR).getall()
            answer_html = " ".join(answer_html).strip()

            # if no question, answer belongs to last question. ("How can I avoid the risk of infection?")
            if (question == ''):
                columns["answer"][-1] += ' ' + answer
                columns["answer_html"][-1] += ' ' + answer_html
                continue

            # add question-answer pair to data dictionary
            columns["question"].append(question)
            columns["answer"].append(answer)
            columns["answer_html"].append(answer_html)

        today = date.today()

        columns["link"] = ["https://www.unicef.org/stories/novel-coronavirus-outbreak-what-parents-should-know"] * len(
            columns["question"])
        columns["name"] = ["Coronavirus disease (COVID-19): What parents should know"] * len(columns["question"])
        columns["source"] = ["UNICEF"] * len(columns["question"])
        columns["category"] = [""] * len(columns["question"])
        columns["country"] = [""] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["en"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns
