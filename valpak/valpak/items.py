# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class ValpakScrapperItem(Item):
    title = Field()
    part_number = Field()
    category = Field()
    manufacturer = Field()
    oem = Field()
    og_manufacturer = Field()
    uom = Field()
    upc = Field()
    sku = Field()
    country = Field()
    image_urls = Field()
    images = Field()

class MartinScrapperItem(Item):
    title = Field()
    part_number = Field()
    category = Field()
    manufacturer = Field()
    oem = Field()
    og_manufacturer = Field()
    uom = Field()
    upc = Field()
    sku = Field()
    country = Field()
    image_urls = Field()
    images = Field()

