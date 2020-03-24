from datetime import date

import scrapy
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = "BVF_scraper"
    start_urls = [
        "https://www.bvf.de/aktuelles/fachliche-meldungen/artikel/news/faq-fuer-schwangere-frauen-und-ihre-familien-zu-spezifischen-risiken-der-covid-19-virusinfektion/"]

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
        QUESTIONS_SELECTOR = ".news-text-wrap h3::text"
        ANSWER_SELECTOR = " ::text"
        ANSWER_HTML_SELECTOR = "*"

        for q in response.css(QUESTIONS_SELECTOR):
            question = q.get()
            answer = ""
            answer_html = ""
            for selector in response.xpath("//div/h3[contains(text(), '" + question + "')]/following-sibling::*"):
                if "h3" in selector.get():
                    break
                else:
                    answer += " ".join(selector.css(ANSWER_SELECTOR).getall()).strip() + "\n"
                    answer_html += " ".join(selector.css(ANSWER_HTML_SELECTOR).getall()).strip()

            columns['question'].append(question)
            columns['answer'].append(answer)
            columns['answer_html'].append(answer_html)

        today = date.today()

        columns["link"] = [
                              "https://www.bvf.de/aktuelles/fachliche-meldungen/artikel/news/faq-fuer-schwangere-frauen-und-ihre-familien-zu-spezifischen-risiken-der-covid-19-virusinfektion/"] * len(
            columns["question"])
        columns["name"] = [
                              "FAQ für schwangere Frauen und ihre Familien zu spezifischen Risiken der COVID-19-Virusinfektion"] * len(
            columns["question"])
        columns["source"] = ["Berufsverband der Frauenärzte (BvF)"] * len(columns["question"])
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
