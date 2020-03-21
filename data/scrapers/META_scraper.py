import scrapy
from scrapy.crawler import CrawlerProcess
import os
import importlib.util


if __name__ == "__main__":
    PATH = os.getcwd()

    crawler_files = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f)) and "META" not in f]
    print(PATH)
    print(os.listdir(os.getcwd()))
    print(crawler_files)
    process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })

    for crawler in crawler_files:
        scraper_spec = importlib.util.spec_from_file_location("CovidScraper", crawler)
        scraper = importlib.util.module_from_spec(scraper_spec)
        scraper_spec.loader.exec_module(scraper)
        CovidScraper = scraper.CovidScraper()
        process.crawl(CovidScraper)
    process.start()
