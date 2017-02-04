# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompetitionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    month = scrapy.Field()
    personal_participate_total = scrapy.Field()
    personal_total = scrapy.Field()
    personal_avg_price = scrapy.Field()
    personal_min_price = scrapy.Field()
    personal_min_price_volume = scrapy.Field()
    personal_min_price_total = scrapy.Field()
    corporate_total = scrapy.Field()
    corporate_participate_total = scrapy.Field()
    corporate_avg_price = scrapy.Field()
    corporate_min_price = scrapy.Field()
    corporate_min_price_volume = scrapy.Field()
    corporate_min_price_total = scrapy.Field()
    table = scrapy.Field()

class LotteryItem(scrapy.Item):
    month = scrapy.Field()
    personal_participate_total = scrapy.Field()
    personal_total = scrapy.Field()
    corporate_total = scrapy.Field()
    corporate_participate_total = scrapy.Field()
    table = scrapy.Field()
