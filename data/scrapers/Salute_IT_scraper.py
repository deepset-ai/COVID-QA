# run 'scrapy runspider Salute_IT_scraper.py' to scrape data

from datetime import date
import scrapy
import pandas as pd
from bs4 import BeautifulSoup

class Salute_IT_Scrapper(scrapy.Spider):
    name = "Salute_IT_Scraper"
    start_urls = ["http://www.salute.gov.it/portale/nuovocoronavirus/dettaglioFaqNuovoCoronavirus.jsp?id=228"]

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

        # extract topics
        for x in response.xpath('//dl'):
            # question is in second strong object in dt
            question_list = [ q.strip() for q in x.xpath('./dt/strong[2]/text()').extract() ]
            # answer is in dd
            answer_html_list = []
            answer_list = []
            for a in x.xpath('./dd')[:-1]:
                answer_html_list.append(' '.join([ h.strip() for h in a.xpath('./p').extract() ]))
                answer_list.append(' '.join([ t.strip() for t in a.xpath('./p/text()').extract() ]))
            if len(question_list) == len(answer_list):
                for question_text, answer_text, answer_html in zip(question_list, answer_list, answer_html_list):
                    columns["question"].append(question_text)
                    columns["answer"].append(answer_text)
                    columns["answer_html"].append(answer_html)

        today = date.today()

        columns["link"] = ["http://www.salute.gov.it/portale/nuovocoronavirus/dettaglioFaqNuovoCoronavirus.jsp?id=228"] * len(columns["question"])
        columns["name"] = ["FAQ - Covid-19, domande e risposte"] * len(columns["question"])
        columns["source"] = ["Ministero della Salute, IT"] * len(columns["question"])
        columns["category"] = [""] * len(columns["question"])
        columns["country"] = ["IT"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["it"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        dataframe = pd.DataFrame(columns)

        dataframe.to_csv("salute_it.tsv", sep="\t", index=False)

