# run 'scrapy runspider FHM_SV_scraper.py' to scrape data

#Add data in English from Folkhälsomyndigheten

import scrapy
from datetime import date
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = 'fhm_en_spyder'
    start_urls = ['https://www.folkhalsomyndigheten.se/the-public-health-agency-of-sweden/communicable-disease-control/covid-19/']

    questionsOnly = True

    def transformContent(self, contentNode):
        responseParts = []
        for responsePart in contentNode.xpath('.//text()').getall():
            strippedPart = responsePart.strip()
            if len(strippedPart) > 0:
                responseParts.append(strippedPart)
        return ' '.join(responseParts)

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


        categoryPaths = response.xpath('//div[@class="container"]')

        for catPath in categoryPaths:

            categoryName = catPath.xpath('./h2/text()').getall()
            #print(categoryName)
            if len(categoryName) == 0:
                continue


            qnaPaths = catPath.xpath('.//*[@class="accordion__item toggle"]')
            for qnaPath in qnaPaths:


                question = qnaPath.xpath('./strong/a/span/text()').getall()


                responseParagraphPaths = qnaPath.xpath('.//div[@class="textbody"]')


                response = ""
                for respParaPath in responseParagraphPaths:
                    response += " ".join(respParaPath.xpath('.//text()').getall()) + "\n\n"

                response = response.strip()

                columns["question"].append(question[0])
                columns["category"].append(categoryName[0])
                columns["answer"].append(response)
                columns["answer_html"].append(" ".join(responseParagraphPaths.getall()))
        today = date.today()


        columns["link"] = ["https://www.folkhalsomyndigheten.se/the-public-health-agency-of-sweden/communicable-disease-control/covid-19/"] * len(columns["question"])
        columns["name"] = ["Q&A on coronaviruses (COVID-19)"] * len(columns["question"])
        columns["source"] = ["FHM, Folkhälsomyndigheten"] * len(columns["question"])
        columns["country"] = ["Sweden"] * len(columns["question"])
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
