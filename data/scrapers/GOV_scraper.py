# run 'scrapy runspider GOV_scraper.py' to scrape data

import scrapy
import numpy as np
from datetime import date
import pandas as pd

class rki_infos(scrapy.Spider):
	name = 'rki_spyder'
	start_urls = ['https://www.gov.pl/web/koronawirus/pytania-i-odpowiedzi']

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

		for x in range(0, len(response.xpath('//summary/text()').extract())):
			question_text = response.xpath('//summary/text()').extract()[x]
			answer_text = "".join(response.xpath('//summary[text()="'+question_text+'"]/following-sibling::node()/descendant-or-self::text()').extract())
			columns['question'].append(question_text)
			columns['answer'].append(answer_text)
		
		today = date.today()

		columns["link"] = ["https://www.gov.pl/web/koronawirus/pytania-i-odpowiedzi"] * len(columns["question"])
		columns["name"] = ["Pytania i odpowiedzi (COVID-19)"] * len(columns["question"])
		columns["source"] = ["GOV Polska (COVID-19)"] * len(columns["question"])
		columns["category"] = [""] * len(columns["question"])
		columns["country"] = ["PL"] * len(columns["question"])
		columns["region"] = [""] * len(columns["question"])
		columns["city"] = [""] * len(columns["question"])
		columns["lang"] = ["pl"] * len(columns["question"])
		columns["answer_html"] = [""] * len(columns["question"])
		columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

		dataframe = pd.DataFrame(columns)
		dataframe.to_csv("gov_pl.tsv", sep="\t", index=False)





