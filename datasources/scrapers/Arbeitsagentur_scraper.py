from datetime import date
import scrapy
import pandas as pd

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
