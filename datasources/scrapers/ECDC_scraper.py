# run 'scrapy runspider ECDC_scraper.py' to scrape data

from datetime import date

import scrapy
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = "ECDCS_scraper"
    start_urls = ["https://www.ecdc.europa.eu/en/novel-coronavirus-china/questions-answers"]

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

        # Scraper Idea: we search for the questions, all paragraphs that follow belong to the question

        QUESTION_ELEMENT_SELECTOR = ".ct--view-30 .text-image h3"
        QUESTION_SELECTOR = "::text"

        questions = response.css(QUESTION_ELEMENT_SELECTOR)
        for question_elm in questions:
            question = question_elm.css(QUESTION_SELECTOR).getall()
            question = " ".join(question).replace('\xa0', ' ')
            # we remove the first 2 chars, they look like this '1.'
            question = question[2:]
            question = question.strip()

            # all paragraphs till the next question header are considert to be the answer
            following_siblings = question_elm.xpath('following-sibling::*')
            answer = []
            answer_html = []
            for elm in following_siblings:
                if elm.root.tag != 'h3':
                    answer += elm.css("::text").getall()
                    answer_html += [elm.get()]
            answer = "".join(answer).replace('\xa0', ' ').strip()
            answer_html = " ".join(answer_html).strip()

            # add question-answer pair to data dictionary
            columns["question"].append(question)
            columns["answer"].append(answer)
            columns["answer_html"].append(answer_html)

        today = date.today()

        columns["link"] = ["https://www.ecdc.europa.eu/en/novel-coronavirus-china/questions-answers"] * len(
            columns["question"])
        columns["name"] = ["Q & A on COVID-19"] * len(columns["question"])
        columns["source"] = ["European Centre for Disease Prevention and Control"] * len(columns["question"])
        columns["category"] = [""] * len(columns["question"])
        columns["country"] = [""] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["en"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        # df = pd.DataFrame(columns)
        return columns


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(CovidScraper)
    process.start()
