from typing import override
from v1.models import Phone, Posting


class Scraper:
    def __init__(self, parser) -> None:
        self.parser = parser

    def scrape(self, phone, depth=1):
        pass


class AmazonScraper(Scraper):
    BASE_URL = "https://www.amazon.in"
    SEARCH_ROUTE = "/s"
    QUERY_PARAM_NAME = "k"

    @override
    def scrape(self, phone, depth=1):
        print("Scraping Amazon")
