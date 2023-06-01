# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogItem(scrapy.Item):
    name = scrapy.Field()
    content = scrapy.Field()
    datetime = scrapy.Field()
    source = scrapy.Field()