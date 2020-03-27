# run 'scrapy runspider BMWI_scraper.py' to scrape data

from datetime import date
import re
import scrapy
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = 'bmwi_spyder'
    start_urls = ['https://www.bmwi.de/Redaktion/DE/FAQ/Coronavirus/faq-coronavirus.html']
		
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

        categoryName = ""
        question = ""
        for elementPath in response.xpath('//div[@class="content"]/div/child::node()'):
            tagName = elementPath.xpath('name()').get()
            if tagName == 'h2':
                categoryName = ' '.join(elementPath.xpath('.//text()').getall()).strip()
            if len(categoryName) == 0:
                continue
            if tagName == 'div':
                question = ' '.join(elementPath.xpath('.//h2//text()').getall()).strip()
                response = ''
                responsePath = elementPath.xpath('.//div[@class="accordion-body collapse"]//div[@class="rich-text"]')
                for path in responsePath.xpath('.//p|.//ul/li'):
                    response += '\n\n' + ' '.join(path.xpath('.//text()').getall())
                response = re.sub('\(Stand[^)]*\)', '', response).strip()
                columns['category'].append(categoryName)
                columns['question'].append(question)
                columns['answer'].append(response)
                columns['answer_html'].append(responsePath.get())

        today = date.today()

        columns["link"] = ["https://www.bmwi.de/Redaktion/DE/FAQ/Coronavirus/faq-coronavirus.html"] * len(columns["question"])
        columns["name"] = ["Coronavirus: Antworten auf häufig gestellte Fragen"] * len(columns["question"])
        columns["source"] = ["Bundesministerium für Wirtschaft und Energie"] * len(columns["question"])
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
