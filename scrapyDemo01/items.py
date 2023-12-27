# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    score = scrapy.Field()
    comment = scrapy.Field()
    actors = scrapy.Field()
    # playable = scrapy.Field()
    # directors = scrapy.Field()
    # actors = scrapy.Field()
    # year = scrapy.Field()
    # country = scrapy.Field()
    # genre = scrapy.Field()
