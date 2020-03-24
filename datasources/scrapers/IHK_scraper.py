from datetime import date
import scrapy
import pandas as pd

class CovidScraper(scrapy.Spider):
    name = "IHK_Scraper"
    start_urls = ["https://www.dihk.de/de/aktuelles-und-presse/coronavirus/faq-19594"]

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
        question_answer_pair = False

        all_nodes = response.xpath("//*")
        for node in all_nodes:
            # save previous question-answer pair
            if question_answer_pair:
                columns["question"].append(current_question)
                columns["answer"].append(current_answer)
                columns["answer_html"].append(current_answer_html)
                columns["category"].append(current_category)
                question_answer_pair = False

            # in category
            if node.attrib.get("class") == "accordion__headline":
                current_category = node.css("::text").get()
                continue

            if current_category:
                # in question
                if node.attrib.get("class") == "accordion__btn-inner":
                    current_question = node.css("::text").get()
                    continue

                # in answer
                if current_question and (node.attrib.get("class") == "rte__content"):
                    current_answer = node.css(" ::text").getall()
                    current_answer = " ".join(current_answer).strip()
                    current_answer_html = node.getall()
                    current_answer_html = " ".join(current_answer_html).strip()
                    question_answer_pair = True
                    continue

            # end of FAQ
            if node.attrib.get("class") == "u-area is-area-cols-2 is-auto-height is-low-margin is-mobile-full":
                break

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
