# run 'scrapy runspider CDC_Pregnancy_scraper.py' to scrape data

from datetime import date

import scrapy


class CovidScraper(scrapy.Spider):
    name = "CDC_Pregnancy_Scraper"
    start_urls = ["https://www.cdc.gov/coronavirus/2019-ncov/prepare/pregnancy-breastfeeding.html"]

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

        found_p = False
        found_question = False
        unnecessary = False
        current_answer = ""
        current_answer_html = ""
        current_category = ""
        current_question = ""

        all_nodes = response.xpath("//*")
        for node in all_nodes:
            # iterate until end of question-answer block
            if node.attrib.get("class") != "row d-none d-lg-block":
                # unnecessary block
                if (node.attrib.get("class") in ["card-body ", "card bt-3 bt-primary mb-3",
                                                 "card bt-3 bt-secondary mb-3"]):
                    unnecessary = True
                    continue

                # get category
                if node.attrib.get("class") == "card-header h4 bg-tertiary":
                    if current_answer:
                        columns["question"].append(current_question)
                        columns["answer"].append(current_answer)
                        columns["answer_html"].append(current_answer_html)
                        columns["category"].append(current_category)
                    current_category = node.css("::text").get()
                    current_question = ""
                    current_answer = ""
                    current_answer_html = ""
                    continue

                # get question
                if (node.xpath("name()").get() == "h4"):
                    unnecessary = False
                    found_question = True
                    if current_answer:
                        columns["question"].append(current_question)
                        columns["answer"].append(current_answer)
                        columns["answer_html"].append(current_answer_html)
                        columns["category"].append(current_category)
                    current_question = node.css("::text").get()
                    current_answer = ""
                    current_answer_html = ""
                    continue

                # get answer
                if found_question and (not unnecessary) and (node.xpath("name()").get() != "a"):
                    answer_part = node.css("::text").getall()
                    current_answer += " ".join(answer_part) + " "
                    answer_part_html = node.get()
                    current_answer_html += answer_part_html
                    continue

            else:
                columns["question"].append(current_question)
                columns["answer"].append(current_answer)
                columns["answer_html"].append(current_answer_html)
                columns["category"].append(current_category)
                break

        today = date.today()

        columns["link"] = ["https://www.cdc.gov/coronavirus/2019-ncov/prepare/pregnancy-breastfeeding.html"] * len(
            columns["question"])
        columns["name"] = ["Pregnancy & Breastfeeding"] * len(columns["question"])
        columns["source"] = ["Center for Disease Control and Prevention (CDC)"] * len(columns["question"])
        columns["category"] = ["Children"] * len(columns["question"])
        columns["country"] = ["USA"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["en"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns
