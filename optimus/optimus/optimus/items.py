# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class Product(Item):
    abbreviation = Field()
    title = Field()
    img_main = Field()
    img_whole = Field()
    imagemap = Field()
    image_urls = Field()
    coords = Field()
    parts = Field()
    images = Field()
    # front page info
    modelid = Field()
    model = Field()
    manufacturer = Field()
    category = Field()
    url = Field()

class Part(Item):
    sku = Field()
    title = Field()
    description = Field()
    manufacturer = Field()
    abbreviation = Field()
    fits_model = Field()
    oem = Field()
    optimus_sku = Field()
    image_urls = Field()
    images = Field()
    dataid = Field()


