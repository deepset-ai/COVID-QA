# run 'scrapy runspider FHM_SV_scraper.py' to scrape data

#Add data in Swedish from Folkhälsomyndigheten

import scrapy
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = 'fhm_sv_spyder'
    start_urls = ['https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/fragor-och-svar/']

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


        categoryPaths = response.xpath('//div[@class="faq-container"]')

        for catPath in categoryPaths:

            categoryName = catPath.xpath('./h2/span/text()').getall()
            #print(categoryName)
            if len(categoryName) == 0:
                continue


            qnaPaths = catPath.xpath('.//*[@class="accordion__item toggle"]')
            for qnaPath in qnaPaths:


                question = qnaPath.xpath('./strong/a/span/span/text()').getall()


                responseParagraphPaths = qnaPath.xpath('.//div[@class="textbody"]')


                response = ""
                for respParaPath in responseParagraphPaths:
                    response += " ".join(respParaPath.xpath('.//text()').getall()) + "\n\n"

                #Cleanup text. It contains a link and a date updated in the text
                response = response.strip()
                splitted = response.split("\n")
                dater = splitted[-2].strip().replace("Uppdaterad: ", "").replace("-", "/").split(" ")[0]
                response = "\n".join(splitted[:-2 or None])

                columns["question"].append(question[0])
                columns["category"].append(categoryName[0])
                columns["answer"].append(response)
                columns["last_update"].append(dater)
                columns["answer_html"].append(" ".join(responseParagraphPaths.getall()))

        columns["link"] = ["https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/fragor-och-svar/"] * len(columns["question"])
        columns["name"] = ["Q&A on coronaviruses (COVID-19)"] * len(columns["question"])
        columns["source"] = ["FHM, Folkhälsomyndigheten"] * len(columns["question"])
        columns["country"] = ["Sweden"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["sv"] * len(columns["question"])

        return columns


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(CovidScraper)
    process.start()
