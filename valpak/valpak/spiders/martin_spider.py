import time
import re
import logging as log
import itertools
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from valpak.items import MartinScrapperItem
from scrapy.spiders import BaseSpider
from scrapy.http import Request, FormRequest
from scrapy.item import Item, Field

from selenium import webdriver
from selenium import selenium
"""
start_urls = [
    'http://martinpump.com/100-series/',
    'http://martinpump.com/liquid-end-100/',
    'http://martinpump.com/motors-100/',
    'http://martinpump.com/martin-100-series-parts/',
    'http://martinpump.com/complete-pumps-500-series/',
    'http://martinpump.com/liquid-end-500-series/',
    'http://martinpump.com/motors-500-series/',
    'http://martinpump.com/martin-500-series-parts/',
    'http://martinpump.com/complete-pumps-600-series/',
    'http://martinpump.com/motor-subassemblies-600-series/',
    'http://martinpump.com/liquid-end-600-series/',
    'http://martinpump.com/motors-600-series/',
    'http://martinpump.com/martin-600-series-parts/'
]
"""


class MartinSpider(Spider):


    name = "martin"
    allowed_domains = ['val-pakproducts.com']
    start_urls = [
        'http://martinpump.com/complete-pumps-100/'
    ]


    def parse(self, response):
        hxs = Selector(response)
        item = MartinScrapperItem()

        try:
            titles = hxs.xpath(
                '//div[@class="wpb_wrapper"]//div[@class="wpb_wrapper"]/text()'
            ).extract()
            print(titles)
            clean_titles = [
                ct for ct in [
                    re.sub(r'\s+',' ',title).strip() for title in titles
                ] if ct
            ]
            info_list = hxs.xpath(
                    '//div[@class="wpb_wrapper"]//div[@class="wpb_wrapper"]/p/text()'
            ).extract()
            clean_info_list = [
                ct for ct in [
                    re.sub(r'\s+',' ',info).strip() for info in info_list
                ] if ct
            ]
            print(clean_info_list)
            #print(info)
        except KeyError:
            self.log('Unable to find title', level=log.WARNING)
        return item
