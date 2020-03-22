# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GovsalariesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = scrapy.Field()
    Year = scrapy.Field()
    Job_Title = scrapy.Field()
    Employer = scrapy.Field()
    Annual_Wage = scrapy.Field()
    Monthly_Wage = scrapy.Field()

