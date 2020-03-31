import logging
import pandas as pd
from scrapy.crawler import CrawlerProcess
from datasources.automatic.testing_WHO_scraper import CovidScraper

logger = logging.getLogger(__name__)


def scrape(url):
    # try to extract question and answer for each url
    questions, answers = "q","a" # do scraping here
    return questions, answers


########## TESTING CODE
RESULTS = []
class Pipeline(object):
    def process_item(self, item, spider):
        df = pd.DataFrame.from_dict(item)
        RESULTS.append(df)

def get_test_data():
    # Code for getting the test set of questions and answers
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': {'__main__.Pipeline': 1}
    })
    process.crawl(
        CovidScraper)  # uses the WHO manual scraper with version fixed through waybackmachine (see import above)
    process.start()
    dataframe = pd.concat(RESULTS)
    questions_truth = dataframe.question
    answers_truth = dataframe.answer
    return questions_truth,answers_truth
######### END TESTING CODE

if __name__ == "__main__":
    logging.disable(logging.WARNING)
    questions_truth, answers_truth = get_test_data()
    print(questions_truth)

    # for the intelligent scraper, a fixed version of WHO website is used so results coming back from get_test_data can be fixed
    #urls = ["https://www.who.int/news-room/q-a-detail/q-a-coronaviruses"]
    urls = ["https://web.archive.org/web/20200331131108/https://www.who.int/news-room/q-a-detail/q-a-coronaviruses"]
    questions_auto, answers_auto = scrape(urls)

    # check weather questions_truth is similar to questions_auto,
    # and answers_truth similar to answers_auto



