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
import sys
import signal

from selenium import webdriver, selenium
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
"""
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from optimus.items import OptimusScrapperItem
from scrapy.spiders import BaseSpider
from scrapy.http import Request, FormRequest
from scrapy.item import Item, Field
"""

def sigint(signal, frame):
    sys.exit(0)

def make_waitfor_elem_updated_predicate(driver, waitfor_elem_xpath):
    elem = driver.find_element_by_xpath(waitfor_elem_xpath)

    def elem_updated(driver):
        try:
            elem.text
        except StaleElementReferenceException:
            return False
        except:
            pass

        return True

    return lambda driver: elem_updated(driver)

class Scraper(object):


    name = 'optimus'
    """
    allowed_domains = ['http://www.optimusparts.com/']
    #start_urls = ['http://val-pakproducts.com/products/?_sft_product_cat=miscellaneous-premier-parts']
    start_urls = ['http://www.optimusparts.com/shop']
    rules = (
        # Extract product links so that parse_items can scrap the appropriate data for each product.
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="row"]/ul[@class="products"]//a[@class="main-link"]',)), callback='parse_items', follow=True),

        # Extract links so that the web crawler can move to the next page.
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="next page-numbers"]',))),
    )
    """
    manufacturer_select_xpath = '//select[@id="ddlMfgMfg"]'
    categories_select_xpath = '//select[@id="ddlMfgCat"]'
    main_categories_select_xpath = '//select[@id="ddlCatCat"]'


    def __init__(self):
        #CrawlSpider.__init__(self)
        self.driver = webdriver.Firefox()
        self.url = 'http://www.optimusparts.com/shop'

    def __del__(self):
        self.driver.close()
        #CrawlSpider.__del__(self)

    def load_page(self):
        self.driver.get(self.url)

        def page_loaded(driver):
            return driver.find_element_by_xpath(self.manufacturer_select_xpath)

        wait = WebDriverWait(self.driver, 10)
        wait.until(page_loaded)

    def get_select(self, xpath):
        select_elem = self.driver.find_element_by_xpath(xpath)
        return Select(select_elem)

    def select_option(self, value, xpath, waitfor_elem_xpath=None):
        if waitfor_elem_xpath:
            func = make_waitfor_elem_updated_predicate(
                self.driver,
                waitfor_elem_xpath
            )
        select = self.get_select(xpath)
        select.select_by_value(value)
        if waitfor_elem_xpath:
            wait = WebDriverWait(self.driver, 10)
            wait.until(func)
        return self.get_select(xpath)

    def make_select_option_iterator(self, xpath, waitfor_elem_xpath):
        def next_option(xpath, waitfor_elem_xpath):
            try:
                select = self.get_select(xpath)
                selection_option_values = [
                    '{}'.format(option.get_attribute('value'))
                    for option in select.options if option.text != 'Choose One'
                ]
                for value in selection_option_values:
                    if waitfor_elem_xpath:
                        select = self.select_option(value, xpath, waitfor_elem_xpath)
                    #yield select.first_selected_option.text
                    yield value
            except StaleElementReferenceException:
                next_option(xpath, waitfor_elem_xpath)



        return lambda: next_option(xpath, waitfor_elem_xpath)

    def get_elements_by_xpath(self, xpath):
        links = self.driver.find_elements_by_xpath(xpath)

    def scrape(self):
        manufacturers = self.make_select_option_iterator(
            self.manufacturer_select_xpath,
            self.categories_select_xpath
        )

        categories = self.make_select_option_iterator(
            self.categories_select_xpath,
            None
        )

        products = self.get_elements_by_xpath(
            '//a[@class="button-details"]'
        )

        self.load_page()
        adict = {}
        for manufacturer in manufacturers():
            if not manufacturer in adict:
                adict[manufacturer] = []
            self.driver.implicitly_wait(3)
            for category in categories():
                if category not in adict[manufacturer]:
                    link = "http://www.optimusparts.com/shop/models.aspx?\
                            CategoryId={1}\
                            &ManufacturerId={0}".format(manufacturer, category)
                    print link
                    adict[manufacturer].append(category)
                self.driver.implicitly_wait(1)
        print adict



"""
PSEUDO CODE:
load category page
for each link, follow
in each link
    - grab the main product information.
    - grab the pdf and map if available
    - click the popup link for each part
    - grab each part's information
    - store each part under the main products information.
"""





if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint)
    scraper = Scraper()
    scraper.scrape()
