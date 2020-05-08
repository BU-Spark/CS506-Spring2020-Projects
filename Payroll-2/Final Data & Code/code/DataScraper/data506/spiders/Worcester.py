import scrapy
from data506.items import Data506Item


class WorcesterSpider(scrapy.Spider):
    name = 'Worcester'
    allowed_domains = ['govsalaries.com']
    
    start_urls = ['http://govsalaries.com/']
    url = 'https://govsalaries.com/salaries/MA/city-of-worcester?year={year}&page={page}'

    def start_requests(self):
        for page in range(1, 124):
            yield scrapy.Request(url=self.url.format(year=2018, page=page),
                                 callback=self.parse_website, dont_filter=True)

        for page in range(1, 122):
            yield scrapy.Request(url=self.url.format(year=2017, page=page),
                                 callback=self.parse_website, dont_filter=True)

        for page in range(1, 98):
            yield scrapy.Request(url=self.url.format(year=2016, page=page),
                                 callback=self.parse_website, dont_filter=True)

        for page in range(1, 30):
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
        item = Data506Item()
        item['Name'] = response.meta['name']
        item['Year'] = response.meta['year']
        item['Job_Title'] = response.meta['job_title']
        item['Employer'] = response.meta['employer']
        third = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[3]//td[1]') \
            .xpath('string(.)').extract_first(default='')

        if 'Original Job Title' in third:
            
            fifth = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[5]//a') \
                .xpath('string(.)').extract_first(default='')
            if fifth:
                item['Annual_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[8]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')
                
            else:
                item['Annual_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[7]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')
        else:
            fourth = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[4]//a') \
                .xpath('string(.)').extract_first(default='')
            if fourth:
                item['Annual_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[7]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')

            else:
                item['Annual_Wage'] = response.xpath('//table[@class="table table-condensed FirstBold"]//tr[6]//td[2]') \
                    .xpath('string(.)').extract_first(default='').strip('$')
                
        yield item
