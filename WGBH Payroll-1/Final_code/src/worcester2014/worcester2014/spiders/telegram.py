# -*- coding: utf-8 -*-
import scrapy
from worcester2014.items import Worcester2014Item


class TelegramSpider(scrapy.Spider):
    name = 'telegram'
    allowed_domains = ['https://www.telegram.com/']
    start_urls = ['https://www.telegram.com/assets/apgraphics/2015/Salaries/Worc-2014-Salaries.html/']
    url = 'https://www.telegram.com/assets/apgraphics/2015/Salaries/Worc-2014-Salaries.html'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        item = Worcester2014Item()
        rows = response.xpath('/html/body/table//tr')
        # print("There are " + str(len(rows)) + " rows")
        # print(rows)
        for i in range(5, len(rows)):
            item['Rank_Gross_Pay'] = rows[i].xpath('./td[1]').xpath('string(.)').extract_first()
            item['Last_Name'] = rows[i].xpath('./td[2]').xpath('string(.)').extract_first()
            item['First_Name'] = rows[i].xpath('./td[3]').xpath('string(.)').extract_first()
            item['Job_Title'] = rows[i].xpath('./td[4]').xpath('string(.)').extract_first()
            item['Gross_Pay'] = rows[i].xpath('./td[5]').xpath('string(.)').extract_first()
            item['Regular_Pay'] = rows[i].xpath('./td[6]').xpath('string(.)').extract_first()
            item['Pay_Detail'] = rows[i].xpath('./td[7]').xpath('string(.)').extract_first()
            item['OT'] = rows[i].xpath('./td[8]').xpath('string(.)').extract_first()
            yield item
