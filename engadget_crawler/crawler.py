# -*- coding: utf-8 -*-

from __future__ import print_function
from engadget_crawler.scraper import EngadgetScraper
from bs4 import BeautifulSoup

import time

try:
    from urllib.request import urlopen
    from urllib.parse import urljoin
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen
    from ullib2 import urljoin
    from urllib2 import HTTPError


class EngadgetCrawler:

    page_count = 1
    FINISH_CRAWL = "Finish crawl!"

    base_url = "https://engadget.com/"

    def __init__(self, target_url, save_dir="./data"):
        self.target_url = target_url
        self.before_url = None
        self.save_dir = save_dir

    def _make_soup(self, url):
        try:
            with urlopen(url) as response:
                html = response.read()

            return BeautifulSoup(html, "lxml")

        except HTTPError as e:
            print("[ DEBUG ] in WiredCrawler#make_soup: {}".format(e))
            return None

    def get_next_page_link(self, url):

        self.before_url = url
        soup = self._make_soup(self.target_url)
        a_next = soup.find("a", {"class": "o-btn--small"})

        if a_next is not None and "href" in a_next.attrs:
            abs_next_page_url = a_next["href"]
            next_page_url = urljoin(self.base_url, abs_next_page_url)

            if self.before_url != next_page_url:
                print("[ DEBUG ] Next article list page: {}".format(url))
                return next_page_url

        return None

    def crawl(self):

        while True:
            print("[ DEBUG ] Now page {} PROCESSING".format(self.page_count))
            scraper = EngadgetScraper(self.target_url, self.save_dir)
            scraper.scrap()
            self.target_url = self.get_next_page_link(self.target_url)

            if self.target_url is None:
                break

            self.page_count += 1
            time.sleep(2)

        return self.FINISH_CRAWL