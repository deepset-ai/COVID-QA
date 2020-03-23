from datetime import date
import scrapy
import pandas as pd

class CovidScraper(scrapy.Spider):
    name = "Berliner_Senat_Scraper"
    start_urls = ["https://www.berlin.de/corona/faq/"]

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




