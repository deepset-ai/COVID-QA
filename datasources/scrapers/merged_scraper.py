from datetime import date
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess

class CovidScraper(scrapy.Spider):
    name = "Arbeitsagentur_Scraper"
    start_urls = ["https://www.arbeitsagentur.de/corona-faq"]

    def parse(self, response):
        columns = {
            "question" : [],
            "answer" : [],
            "answer_html" : [],
            "link" : [],
            "name" : [],
            "source" : [],
            "category" : [],
            "country" : [],
            "region" : [],
            "city" : [],
            "lang" : [],
            "last_update" : [],
        }

        current_category = ""
        current_question = ""
        current_answer = ""
        current_answer_html = ""
        ba_content_article_count = 0

        all_nodes = response.xpath("//*")
        for node in all_nodes:
            if node.attrib.get("class") == "ba-content-row":
                ba_content_article_count += 1
                # end of FAQ
                if ba_content_article_count == 4:
                    break

            # in question
            if node.attrib.get("class") == "collapsed":
                # save previous question-answer pair
                if current_question:
                    columns["question"].append(current_question)
                    columns["answer"].append(current_answer)
                    columns["answer_html"].append(current_answer_html)
                current_question = node.css("::text").get().strip()
                continue

            # in answer
            if node.attrib.get("class") == "ba-copytext":
                current_answer = node.css(" ::text").getall()
                current_answer = " ".join(current_answer).strip()
                current_answer_html = node.getall()
                current_answer_html = " ".join(current_answer_html).strip()
                continue



        columns["question"].append(current_question)
        columns["answer"].append(current_answer)
        columns["answer_html"].append(current_answer_html)

        today = date.today()

        columns["link"] = ["https://www.arbeitsagentur.de/corona-faq"] * len(columns["question"])
        columns["name"] = ["FAQ: Corona-Virus"] * len(columns["question"])
        columns["source"] = ["Bundesagentur für Arbeit"] * len(columns["question"])
        columns["category"] = [""] * len(columns["question"])
        columns["country"] = ["DE"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["de"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns

class CovidScraper(scrapy.Spider):
    name = "BAUA_scraper"
    start_urls = ["https://www.baua.de/DE/Themen/Arbeitsgestaltung-im-Betrieb/Biostoffe/FAQ/FAQ_node.html"]

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
        QUESTIONS_SELECTOR = "//div[@class='tabs-container']/h2[@class='heading']"
        QUESTION_SELECTOR = " ::text"
        ANSWERS_SELECTOR = "//div[@class='tabs-container']/div"
        ANSWER_SELECTOR = "*::text"
        ANSWER_HTML_SELECTOR = "*"

        for q in response.xpath(QUESTIONS_SELECTOR):
            question = q.css(QUESTION_SELECTOR).getall()
            question = " ".join(question).strip()

            columns["question"].append(question)

        for a in response.xpath(ANSWERS_SELECTOR):
            answer = a.css(ANSWER_SELECTOR).getall()
            answer = " ".join(answer).strip()
            answer_html = a.css(ANSWER_HTML_SELECTOR).getall()
            answer_html = " ".join(answer_html).strip()

            columns["answer"].append(answer)
            columns["answer_html"].append(answer_html)

        today = date.today()

        columns["link"] = [
                              "https://www.baua.de/DE/Themen/Arbeitsgestaltung-im-Betrieb/Biostoffe/FAQ/FAQ_node.html"] * len(
            columns["question"])
        columns["name"] = ["Antworten auf häufig gestellte Fragen zu beruflichen Tätigkeiten mit SARS-CoV-2"] * len(
            columns["question"])
        columns["source"] = ["Bundesanstalt für Arbeitsschutz und Arbeitsmedizin (BAuA)"] * len(columns["question"])
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


    class CovidScraper(scrapy.Spider):
        name = "Berliner_Senat_Scraper"
        start_urls = ["https://www.berlin.de/corona/faq/"]

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
            current_question = ""
            current_answer = ""
            current_answer_html = ""
            question_answer_pair = False

            all_nodes = response.xpath("//*")
            for node in all_nodes:
                # in category
                if (node.xpath("name()").get() == "h2") and (node.attrib.get("class") == "title"):
                    current_category = node.css("::text").get()
                    continue

                if current_category:
                    # in question-answer pair
                    if node.attrib.get("class") == "html5-section block module-faq land-toggler":
                        # save previous question-answer pair
                        if current_question:
                            columns["question"].append(current_question)
                            columns["answer"].append(current_answer)
                            columns["answer_html"].append(current_answer_html)
                            columns["category"].append(current_category)

                        question_answer_pair = True
                        continue

                    # in question
                    if question_answer_pair and (node.attrib.get("class") == "land-toggler-button collapsed"):
                        current_question = node.css("::text").get()
                        continue

                    # in answer
                    if question_answer_pair and (node.attrib.get("class") == "textile"):
                        current_answer = node.css(" ::text").getall()
                        current_answer = " ".join(current_answer).strip()
                        current_answer_html = node.getall()
                        current_answer_html = " ".join(current_answer_html).strip()
                        continue

                # end of FAQ
                if node.attrib.get("class") == "html5-section block modul-text_bild":
                    break

            columns["question"].append(current_question)
            columns["answer"].append(current_answer)
            columns["answer_html"].append(current_answer_html)
            columns["category"].append(current_category)

            today = date.today()

            columns["link"] = ["https://www.berlin.de/corona/faq/"] * len(columns["question"])
            columns["name"] = ["Corona-Prävention in Berlin – Fragen und Antworten"] * len(columns["question"])
            columns["source"] = ["Berliner Senat"] * len(columns["question"])
            columns["country"] = ["DE"] * len(columns["question"])
            columns["region"] = ["Berlin"] * len(columns["question"])
            columns["city"] = ["Berlin"] * len(columns["question"])
            columns["lang"] = ["de"] * len(columns["question"])
            columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

            return columns





