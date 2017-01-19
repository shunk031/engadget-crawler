# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.pardir)

from engadget_crawler.scraper import EngadgetScraper

if __name__ == '__main__':

    ENGADGET_URL = "https://www.engadget.com/topics/science/page/1"
    scraper = EngadgetScraper(ENGADGET_URL, "./dump_files")
    scraper.scrap()
