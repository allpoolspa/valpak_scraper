"""This program crawls the val-pakproducts site. It grabs the product
information, which can be seen in items.py.

It uses Scrapy and Selenium. We use selenium due to some js loaded data.

We use a Firefox webdriver for the selenium app.

HOW IT WORKS:
This is a CrawlSpider that starts at val-pakproducts.com/products, then
using the rules it goes to each product detail page on a given product list
page and grabs the relevant information and goes to the next page in
the product search results and repeats until all products have been scrapped.
"""

import time
import re
import logging as log
import itertools
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from valpak.items import ValpakScrapperItem
from scrapy.spiders import BaseSpider
from scrapy.http import Request, FormRequest
from scrapy.item import Item, Field

from selenium import webdriver
from selenium import selenium

class ValpakSpider(CrawlSpider):


    name = 'valpak'
    allowed_domains = ['val-pakproducts.com']
    #start_urls = ['http://val-pakproducts.com/products/?_sft_product_cat=miscellaneous-premier-parts']
    start_urls = ['http://val-pakproducts.com/products/']
    rules = (
        # Extract product links so that parse_items can scrap the appropriate data for each product.
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="row"]/ul[@class="products"]//a[@class="main-link"]',)), callback='parse_items', follow=True),

        # Extract links so that the web crawler can move to the next page.
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="next page-numbers"]',))),
    )


    def parse_items(self, response):
        """This gets the product info that we need from the products
        page. It calls _get_availability(), which selenium handles.
        """
        hxs = Selector(response)
        item = ValpakScrapperItem()
        #Get the fields we need
        try:
            item['title'] = hxs.xpath(
                '//h1[@class="product_title entry-title"]/text()'
            ).extract()[0]
        except KeyError:
            self.log('Unable to find title', level=log.WARNING)
        try:
            item['sku'] = hxs.xpath(
                '//span[@class="sku"]/text()'
            ).extract()[0]
            item['upc'] = item['sku'].replace('.','')
            self.log('Found sku', level=log.INFO)
        except KeyError:
            self.log('Unable to find sku', level=log.WARNING)
        try:
            item['category'] = hxs.xpath(
                '//span[@class="posted_in"]/a/text()'
            ).extract()[0]
        except KeyError:
            self.log('Unable to find category', level=log.WARNING)
        try:
            attributes = hxs.xpath(
                '//table[@class="shop_attributes"]'
            )
        except KeyError:
            self.log(
                'Unable to find table of attributes',
                level=log.WARNING
            )
        try:
            # We need to get the two large images and the thumbnails of the
            # images.
            images = hxs.xpath(
                '//div[contains(@class,"single-product-main-images")]//img/@src'
            ).extract()
            item['image_urls'] = images
        except KeyError:
            self.log(
                'Unable to find images',
                level=log.WARNING
            )
        print(item['sku'])
        self.log(item['sku'])
        #A dictionary that maps the website ids with the items.py ids.
        keymapper = {
            'original manufacturer':'og_manufacturer',
            'oem part number':'oem',
            "val-paks part number": 'part_number',
            "country of origin": "country"
        }
        for attribute in attributes.xpath('//tr'):
            keys = attribute.xpath('//th/text()').extract()
            values = attribute.xpath('//td/p/text()').extract()
            for key, value in itertools.izip(keys, values):
                normalized_key = key.replace("'","").lower()
                try:
                    item[keymapper[normalized_key]] = value
                except KeyError:
                    self.log(
                        'Unable to find %s %s' % (normalized_key, value),
                        level=log.WARNING
                    )
        try:
            part_number = self.get_part_number(item)
            item['part_number'] = part_number
        except:
            print("unable to get part_number...", item)
        try:
            upc = self.clean_upc(item['upc'])
            item['upc'] = upc
        except:
            print("Unable to clean upc...", item)
        try:
            sku = self.create_sku("Val-Pak", item['part_number'])
            item['sku'] = sku
        except:
            print("Unable to make sku...", item)
        try:
            print(item['sku'], item['part_number'])
        except:
            print("Unable to find either sku or part_number", item)
        return item

    def get_part_number(self, item):
        try:
            #val-pak specific: they have two part numbers for some products
            # one is the actual part number
            # and the other is has an S to specify a single uom for ordering.
            part_number = self.clean_part_number(item['part_number'])
        except:
            print("Part Number wasn't found. Using upc instead")
            part_number = self.clean_upc(item['upc'])
        return part_number

    def create_sku(self, manufacturer, part_number):
        return manufacturer[:3].upper() + "_" + part_number

    def clean_part_number(self, part_number):
        """ This is used to clean part numbers."""
        clean_part_number = part_number
        if ',' in part_number:
            value0, value1 = part_number.replace(" ", "").split(',')
            if not value0.endswith('S'):
                clean_part_number = value0
            else:
                clean_part_number = value1
        return clean_part_number

    def clean_upc(self, upc):
        return re.sub("[^0-9]", "", upc)
