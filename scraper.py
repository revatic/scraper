import requests
from lxml import html
import logging
import pandas as pd
from pymongo import MongoClient

BASE_URL = "https://www.zaubacorp.com/company-list-company.html"
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "zaubacorp"
COLLECTION_NAME = "companies"

class Scraper:

    def __init__(self):
        self.logger = self.setup_logger()

    def setup_logger(self):
        '''
         Set up the logger for the ZaubacorpScraper class

         :return: Logger object
         '''
        logger = logging.getLogger("ZaubacorpScraper")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler("scraper.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def get_total_pages(self):
        '''
         Get the total number of pages to scrape by parsing the website
        :return: (int) Total number of pages
        '''
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            total_cnt = tree.xpath(".//span[contains(text(),'Page')]/text()")[0]
            total_page = total_cnt.split('of')[1].replace(',', '')
            return int(total_page)
        else:
            self.logger.error(f"Failed to get response during getting total pages {response.url}")

    def scrape_zaubacorp(self, page_number):
        '''
        Scrape company data from a specific page on Zaubacorp website

        :param page_number: (int) Page number to scrape
        :return: (list) List of dictionaries containing company information
        '''
        url = f'https://www.zaubacorp.com/company-list/p-{page_number}-company.html'
        response = requests.get(url)
        if response.status_code == 200:
            doc = html.fromstring(response.text)
            td = doc.xpath('//table[@id="table"]//tr')
            companies = []

            for data in td:
                name = data.xpath('./td[1]/text()')
                compy = data.xpath('./td[2]//text()')
                roc = data.xpath('./td[3]/text()')
                status = data.xpath('./td[4]/text()')

                if name and compy is not None:
                    companies.append({'name': name[0],
                                      'company': compy[0],
                                      'roc': roc[0],
                                      'status': status[0], })
            return companies
        else:
            self.logger.error(f"Failed to fetch data from page {page_number}")
            return []

    def store_in_mongodb(self,data):
        '''
        Store the scraped company data in MongoDB

        :param data: (list) List of dictionaries containing company information
        :return: None
        '''
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        try:
            collection.insert_many(data)
            self.logger.info(f"Data successfully stored in MongoDB.")
        except Exception as e:
            self.logger.error(f"Error storing data: {str(e)}")
        finally:
            client.close()

    def crawl_and_store(self,limit=10):
        '''
        Main function to initiate the crawling and storing process.

        :param limit: (int) Restrict the number of pages to crawl
        :return:
        '''
        total_pages = self.get_total_pages()
        no_of_pages = min(limit,total_pages)
        companies_info = []
        for page_number in range(1, no_of_pages):
            try:
                companies_on_page = self.scrape_zaubacorp(page_number)
                companies_info.extend(companies_on_page)
                self.logger.info(f"Page {page_number}/{total_pages} scraped successfully.")
            except Exception as e:
                self.logger.error(f"Error scraping data from page {page_number}: {str(e)}")

        if companies_info:
            self.store_in_mongodb(companies_info)


if __name__ == "__main__":
    scraper = Scraper()
    scraper.crawl_and_store()
