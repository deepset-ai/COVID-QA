# run 'scrapy runspider GOV_pl_scraper.py' to scrape data

from datetime import date

import scrapy
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = 'polish_GOV_spyder'
    start_urls = ['https://www.gov.pl/web/koronawirus/pytania-i-odpowiedzi']

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

        for x in range(0, len(response.xpath('//summary/text()').extract())):
            question_text = response.xpath('//summary/text()').extract()[x]
            answer_text = "".join(response.xpath(
                '//summary[text()="' + question_text + '"]/following-sibling::node()/descendant-or-self::text()').extract())
            answer_html = "".join(
                response.xpath('//summary[text()="' + question_text + '"]/following-sibling::node()').extract())

            columns['question'].append(question_text)
            columns['answer'].append(answer_text)
            columns['answer_html'].append(answer_html)

        today = date.today()

        columns["link"] = ["https://www.gov.pl/web/koronawirus/pytania-i-odpowiedzi"] * len(columns["question"])
        columns["name"] = ["Pytania i odpowiedzi (COVID-19)"] * len(columns["question"])
        columns["source"] = ["GOV Polska"] * len(columns["question"])
        columns["category"] = [""] * len(columns["question"])
        columns["country"] = ["PL"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["pl"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(CovidScraper)
    process.start()
