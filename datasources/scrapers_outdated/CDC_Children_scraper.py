# run 'scrapy runspider CDC_Children_scraper.py' to scrape data

from datetime import date
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class CovidScraper(scrapy.Spider):
    name = "CDC_Children_Scraper"
    start_urls = ["https://www.cdc.gov/coronavirus/2019-ncov/prepare/children-faq.html"]

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

        found_p = False
        found_question = False
        current_answer = ""

        categoryPaths = response.xpath('//div[@class="syndicate"]/div[@class="row "]')
        for catPath in categoryPaths:
            categoryName = catPath.xpath('.//h2/text()').getall()
            if len(categoryName) == 0:
                continue;
            categoryName = categoryName[0]
            qnaPaths = catPath.xpath('.//div[@role="tablist"]//div[@class="card"]')
            for qnaPath in qnaPaths:
                question = qnaPath.xpath('.//span[@role="heading"]/text()').get()
                responseParagraphPaths = qnaPath.xpath('.//div[@class="card-body"]')
                response = ""
                for respParaPath in responseParagraphPaths:
                    response += " ".join(respParaPath.xpath('.//text()').getall()) + "\n\n"
                response = response.strip()
                columns["question"].append(question)
                columns["answer"].append(response)
                columns["answer_html"].append(" ".join(responseParagraphPaths.getall()))

        today = date.today()

        columns["link"] = ["https://www.cdc.gov/coronavirus/2019-ncov/prepare/children-faq.html"] * len(
            columns["question"])
        columns["name"] = ["Coronavirus Disease-2019 (COVID-19) and Children"] * len(columns["question"])
        columns["source"] = ["Center for Disease Control and Prevention (CDC)"] * len(columns["question"])
        columns["category"] = ["Children"] * len(columns["question"])
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
