# run 'scrapy runspider CDC_Water_scraper.py' to scrape data

from datetime import date

import scrapy


class CovidScraper(scrapy.Spider):
    name = "CDC_Travel_Scraper"
    start_urls = ["https://www.cdc.gov/coronavirus/2019-ncov/php/water.html"]

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

        found_question = False

        all_nodes = response.xpath("//*")
        for node in all_nodes:
            # in question
            if node.attrib.get("class") == "card-header h4 bg-tertiary":
                found_question = True
                current_question = node.css("::text").get()
                continue

            # in answer
            if found_question and (node.attrib.get("class") == "card-body "):
                current_answer = node.css(" ::text").getall()
                current_answer = " ".join(current_answer).strip()
                current_answer_html = node.getall()
                current_answer_html = " ".join(current_answer_html).strip()

                columns["question"].append(current_question)
                columns["answer"].append(current_answer)
                columns["answer_html"].append(current_answer_html)
            else:
                found_question = False

        columns["question"].append(current_question)
        columns["answer"].append(current_answer)
        columns["answer_html"].append(current_answer_html)

        today = date.today()

        columns["link"] = ["https://www.cdc.gov/coronavirus/2019-ncov/php/water.html"] * len(columns["question"])
        columns["name"] = ["Water Transmission and COVID-19"] * len(columns["question"])
        columns["source"] = ["Center for Disease Control and Prevention (CDC)"] * len(columns["question"])
        columns["category"] = [""] * len(columns["question"])
        columns["country"] = ["USA"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["en"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns
