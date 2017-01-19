# -*- coding: utf-8 -*-

from __future__ import print_function
from bs4 import BeautifulSoup

import os
import csv

try:
    from urllib.request import urlopen
    from urllib.parse import urljoin
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen
    from urllib2 import urljoin
    from urllib2 import HTTPError


class EngadgetScraper:

    base_url = "https://engadget.com/"

    def __init__(self, target_url, save_dir):
        self.target_url = target_url
        self.save_dir = save_dir

    def _make_soup(self, url):
        try:
            with urlopen(url) as response:
                html = response.read()

            return BeautifulSoup(html, "lxml")
        except HTTPError as e:
            print("[ DEBUG ] in {}#make_soup: {}".format(self.__class__.__name__, e))
            return None

    def scrap(self):
        article_detail_url_list = self.get_article_detail_urls()

        article_detail_info = []
        for article_url in article_detail_url_list:
            article_dict = self.get_article_detail_info_dict(article_url)
            article_detail_info.append(article_dict)

        self.save_article_detail_info_list(article_detail_info)

    def get_article_detail_urls(self):

        soup = self._make_soup(self.target_url)

        # 記事概要のそれぞれのデータを取得する
        div_grid_tl = soup.find("div", {"class": "grid@tl+"})
        div_containers = div_grid_tl.find_all("div", {"class": "container@m"})

        # 記事詳細へのURLを取得する
        article_detail_url_list = []
        for i, div_container in enumerate(div_containers):

            if i == 0:
                detail_url = div_container.find("h2").find("a")
            else:
                detail_url = div_container.find("a", {"class": "o-hit__link"})

            try:
                abs_url = detail_url["href"]
                url = urljoin(self.base_url, abs_url)
                print("[ DEBUG ] Get URL: {}".format(url))
                article_detail_url_list.append(url)
            except TypeError:
                pass

        return article_detail_url_list

    def get_article_detail_info_dict(self, article_url):

        article_dict = {}
        article_dict["url"] = article_url

        detail_soup = self._make_soup(article_url)
        title_tag = detail_soup.find("h1", {"class": "t-h4@m-"})
        title = title_tag.get_text()
        print("[ DEBUG ] Title: {}".format(title))
        article_dict["title"] = title

        div_article_texts = detail_soup.find_all("div", {"class": "artcile-text"})
        article_content = [div_article_text.get_text().strip() for div_article_text in div_article_texts]
        article_content = " ".join(article_content)
        article_dict["article"] = article_content

        return article_dict

    def save_article_detail_info_list(self, article_detail_info_list):

        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

        for article_detail_dict in article_detail_info_list:
            article_title = article_detail_dict["title"]
            csv_filename = self._convert_filename(article_title)
            csv_filename = "{}.csv".format(csv_filename)

            with open(os.path.join(self.save_dir, csv_filename), "w") as wf:
                writer = csv.writer(wf)
                writer.writerow([article_detail_dict["title"],
                                 article_detail_dict["url"],
                                 article_detail_dict["article"]])

    def _convert_filename(self, article_title):

        filename = article_title.replace(" ", "_")
        filename = filename.replace("/", "")
        filename = filename.replace("?", "")
        return filename
