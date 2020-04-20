# run 'scrapy runspider CDC_General_scraper.py' to scrape data

from datetime import date

import scrapy
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = "CDC_Scraper"
    start_urls = ["https://www.cdc.gov/coronavirus/2019-ncov/faq.html"]

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

        current_category = ""

        all_nodes = response.xpath("//*")
        for i,node in enumerate(all_nodes):
            # in category
            if node.attrib.get("class") == "onThisPageAnchor":
                current_category = node.attrib["title"]
                continue

            # in category
            if current_category:
                # in question
                if node.attrib.get("role") == "heading":
                    current_question = node.css("::text").get()

                # in answer
                if node.attrib.get("class") == "card-body":
                    current_answer = node.css(" ::text").getall()
                    current_answer = " ".join(current_answer).strip()
                    current_answer_html = node.getall()
                    current_answer_html = " ".join(current_answer_html).strip()

                    # add question-answer-pair to data dictionary
                    columns["question"].append(current_question)
                    columns["answer"].append(current_answer)
                    columns["answer_html"].append(current_answer_html)
                    columns["category"].append(current_category)

            # end of category
            if node.attrib.get("class") == "row":
                current_category = ""

        today = date.today()

        columns["link"] = ["https://www.cdc.gov/coronavirus/2019-ncov/faq.html"] * len(columns["question"])
        columns["name"] = ["CDC General FAQ"] * len(columns["question"])
        columns["source"] = ["Center for Disease Control and Prevention (CDC)"] * len(columns["question"])
        columns["country"] = ["USA"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["en"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns



if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(CovidScraper)
    process.start()
