# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.pardir)

from engadget_crawler.crawler import EngadgetCrawler

if __name__ == '__main__':

    ENGADGET_URL = "https://www.engadget.com/topics/science/page/1"
    crawler = EngadgetCrawler(ENGADGET_URL)
    crawler.crawl()
