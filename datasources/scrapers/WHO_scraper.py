# run 'scrapy runspider WHO_scraper.py' to scrape data

from datetime import date

import scrapy


class CovidScraper(scrapy.Spider):
    name = "WHO_scraper"
    start_urls = ["https://www.who.int/news-room/q-a-detail/q-a-coronaviruses",
                  "https://www.who.int/news-room/q-a-detail/q-a-on-covid-19-and-pregnancy-and-childbirth",
                  "https://www.who.int/news-room/q-a-detail/q-a-on-covid-19-and-breastfeeding",
                  "https://www.who.int/news-room/q-a-detail/q-a-on-covid-19-and-masks",
                  "https://www.who.int/news-room/q-a-detail/q-a-on-covid-19-hiv-and-antiretrovirals",
                  "https://www.who.int/news-room/q-a-detail/q-a-on-mass-gatherings-and-covid-19",
                  "https://www.who.int/news-room/q-a-detail/q-a-on-infection-prevention-and-control-for-health-care-workers-caring-for-patients-with-suspected-or-confirmed-2019-ncov",
                  "https://www.who.int/news-room/q-a-detail/be-active-during-covid-19",
                  "https://www.who.int/news-room/q-a-detail/malaria-and-the-covid-19-pandemic",
                  "https://www.who.int/news-room/q-a-detail/violence-against-women-during-covid-19",
                  "https://www.who.int/news-room/q-a-detail/contraception-family-planning-and-covid-19"]

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

        columns["link"] = [response.url] * len(columns["question"])
        columns["name"] = ["Q&A on coronaviruses (COVID-19)"] * len(columns["question"])
        columns["source"] = ["World Health Organization (WHO)"] * len(columns["question"])
        columns["category"] = [""] * len(columns["question"])
        columns["country"] = [""] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["en"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns
