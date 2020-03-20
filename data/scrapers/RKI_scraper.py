# run 'python -m scrapy crawl rki_spyder -o rki_info.csv' to scrape data

import scrapy
import numpy as np

class rki_infos(scrapy.Spider):
	name = 'rki_spyder'
	start_urls = ['https://www.rki.de/SharedDocs/FAQ/NCOV2019/FAQ_Liste.html']

	def parse(self, response):
		for x in response.xpath('//div[@class="alt-accordion-box-box"]/@id').extract():
			question_id = x
			question_text = response.xpath(str('//*[@id="'+x+'"]/h2/text()')).extract()
			date_update = response.xpath(str('//*[@id="'+x+'"]/div/p[@class="date"]/text()')).extract()
			answer_text = " ".join(response.xpath(str('//*[@id="'+x+'"]/div/p')).xpath('string()').extract())
			source = "https://www.rki.de/SharedDocs/FAQ/NCOV2019/FAQ_Liste.html"

			yield({
				'question_id_rki':question_id,
				'question_text':question_text,
				'date_update':date_update,
				'answer': answer_text,
				'source': source
				})




