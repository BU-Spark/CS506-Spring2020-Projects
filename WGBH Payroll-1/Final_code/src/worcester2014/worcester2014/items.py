# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Worcester2014Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Rank_Gross_Pay = scrapy.Field()
    Last_Name = scrapy.Field()
    First_Name = scrapy.Field()
    Job_Title = scrapy.Field()
    Gross_Pay = scrapy.Field()
    Regular_Pay = scrapy.Field()
    Pay_Detail = scrapy.Field()
    OT = scrapy.Field()

