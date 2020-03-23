# run 'scrapy runspider KBV_scraper.py' to scrape data

from datetime import date

import scrapy
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = 'kbv_spyder'
    start_urls = ['https://www.kbv.de/html/coronavirus.php']

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

        # collect categories
        categoryPaths = {}
        categoryNames = {}
        for categoryPath in response.xpath('//div[@class="grid-2 item-main"]/div[@class="grids-fluid"]'):
            categoryId = categoryPath.xpath('./@id').getall()
            if len(categoryId) == 0:
                continue
            categoryId = categoryId[0]
            if not categoryId.startswith('content'):
                continue
            categoryName = categoryPath.xpath('./div/article/h3/text()').getall()
            if len(categoryName) == 0:
                continue
            categoryName = categoryName[0]
            categoryPaths[categoryId] = categoryPath
            categoryNames[categoryId] = categoryName

        # collect Q&A per category
        for categoryId, catPath in categoryPaths.items():
            categoryName = categoryNames[categoryId]
            for path in catPath.xpath('./div/article/section/dl/dt'):
                questionId = path.xpath('./@id').getall()
                if len(questionId) == 0:
                    continue
                questionId = questionId[0]
                question = " ".join(path.xpath('./text()').getall()).strip()
                if self.questionsOnly and "?" != question[-1]:
                    continue
                responsePath = path.xpath("./following-sibling::dd[1]")
                response = self.transformContent(responsePath)
                columns['category'].append(categoryName)
                columns['question'].append(question)
                columns['answer'].append(response)
                columns['answer_html'].append(responsePath.get())

        today = date.today()

        columns["link"] = ["https://www.kbv.de/html/coronavirus.php"] * len(columns["question"])
        columns["name"] = ["Q&A on coronaviruses (COVID-19)"] * len(columns["question"])
        columns["source"] = ["Kassenärztliche Bundesvereinigung KdöR"] * len(columns["question"])
        columns["country"] = ["DE"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["de"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(CovidScraper)
    process.start()
