import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import importlib.util
import pandas as pd

PATH = os.getcwd()
RESULTS = []

class Pipeline(object):
    def process_item(self, item, spider):
        RESULTS.append(pd.DataFrame.from_dict(item))

if __name__ == "__main__":
    crawler_files = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f)) and "META" not in f]
    process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'ITEM_PIPELINES': {'__main__.Pipeline': 1}
        })
    for crawler in crawler_files:
        scraper_spec = importlib.util.spec_from_file_location("CovidScraper", crawler)
        scraper = importlib.util.module_from_spec(scraper_spec)
        scraper_spec.loader.exec_module(scraper)
        CovidScraper = scraper.CovidScraper
        process.crawl(CovidScraper)
    process.start()
    df = pd.concat(RESULTS)
    df.drop_duplicates(inplace=True)

    #df.to_csv("../faqs/faq_200322_16.tsv", sep="\t", index=False)
