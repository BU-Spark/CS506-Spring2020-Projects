# -*- coding: utf-8 -*-
import scrapy
from govSalaries.items import GovsalariesItem


class BrocktonSpider(scrapy.Spider):
    name = 'Brockton'
    allowed_domains = ['govsalaries.com']
    start_urls = ['http://govsalaries.com/']
    url = 'https://govsalaries.com/salaries/MA/city-of-brockton?year={year}&page={page}'

    def start_requests(self):
        for page in range(1, 71):
            yield scrapy.Request(url=self.url.format(year=2018, page=page),
                                 callback=self.parse_website, dont_filter=True)

        for page in range(1, 72):
            yield scrapy.Request(url=self.url.format(year=2017, page=page),
                                 callback=self.parse_website, dont_filter=True)

        for page in range(1, 76):
            yield scrapy.Request(url=self.url.format(year=2015, page=page),
                                 callback=self.parse_website, dont_filter=True)

    def parse_website(self, response):
        employees = response.xpath('//table[@class="table table-hover table-sm "]//tr[@itemprop="employee"]')
        for employee in employees:
            name = employee.xpath('./td[2]').xpath('string(.)').extract_first(default='').strip()
            year = employee.xpath('./td[3]').xpath('string(.)').extract_first(default='').strip()
            job_title = employee.xpath('./td[4]').xpath('string(.)').extract_first(default='').strip()
            employer = employee.xpath('./td[5]').xpath('string(.)').extract_first(default='').strip()
            details = employee.xpath('./td[6]/a')
            detail_url = details.xpath('./@href').extract_first(default='')
            full_url = response.urljoin(detail_url)
            yield scrapy.Request(url=full_url,
                                 meta={'name': name, 'year': year, 'job_title': job_title, 'employer': employer},
                                 callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        item = GovsalariesItem()
        item['Name'] = response.meta['name']
        item['Year'] = response.meta['year']
        item['Job_Title'] = response.meta['job_title']
        item['Employer'] = response.meta['employer']
        third_row = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[3]//td[1]') \
            .xpath('string(.)').extract_first(default='')
        if 'Original Job Title' in third_row:
            fifth_row = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[5]//a') \
                .xpath('string(.)').extract_first(default='')
            if fifth_row:
                item['Annual_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[8]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')
                item['Monthly_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[9]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')
            else:
                item['Annual_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[7]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')
                item['Monthly_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[8]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')
        else:
            forth_row = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[4]//a') \
                .xpath('string(.)').extract_first(default='')
            if forth_row:
                item['Annual_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[7]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')
                item['Monthly_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[8]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')
            else:
                item['Annual_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[6]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')
                item['Monthly_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[7]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')
        yield item

