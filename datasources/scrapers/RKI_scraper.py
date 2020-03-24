# run 'scrapy runspider RKI_scraper.py' to scrape data

from datetime import date

import scrapy
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = 'rki_spyder'
    start_urls = ['https://www.rki.de/SharedDocs/FAQ/NCOV2019/FAQ_Liste.html']

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

        for x in response.xpath('//div[@class="alt-accordion-box-box"]/@id').extract():
            question_text = response.xpath(str('//*[@id="' + x + '"]/h2/text()')).extract()[0]
            answer_text = " ".join(response.xpath(str('//*[@id="' + x + '"]/div/p')).xpath('string()').extract())
            answer_html = " ".join(response.xpath(str('//*[@id="' + x + '"]/div/p')).extract())

            columns['question'].append(question_text)
            columns['answer'].append(answer_text)
            columns['answer_html'].append(answer_html)

        today = date.today()

        columns["link"] = ["https://www.rki.de/SharedDocs/FAQ/NCOV2019/FAQ_Liste.html"] * len(columns["question"])
        columns["name"] = ["Q&A on coronaviruses (COVID-19)"] * len(columns["question"])
        columns["source"] = ["Robert Koch Institute (RKI)"] * len(columns["question"])
        columns["category"] = [""] * len(columns["question"])
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
