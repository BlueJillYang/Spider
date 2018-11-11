# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from ..items import LagouJobsItem
import time
from lxml import etree


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com/jobs/']
    start_urls = ['http://www.lagou.com/jobs/list_python?px=default&city=%E8%8B%8F%E5%B7%9E']
    # driver = webdriver.Firefox()

    def parse(self, response):
        # self.driver.get(self.start_urls[0])
        # positions_links = []
        # while True:
        #     html = self.driver.page_source
        #     xml = etree.HTML(html)
        #     if html.find('pager_next_disabled'):
        #         break
        #     else:
        #         pass
        #     # 职位链接
        #     positions_links = self.driver.find_elements_by_xpath('//a[@class="position_link"/@href]')
        #
        #     # 获取下一页
        #     self.get_next_page()
        #     positions_links += xml.xpath('//a[@class="position_link"]/@href').extract()
        position_links = response.xpath('//a[@class="position_link"]/@href').extract()
        print(response)
        print('links', position_links)
        for link in position_links:
            yield scrapy.Request(url=link, callback=self.parse_job)

    def parse_job(self, response):
        item = LagouJobsItem()

        item['job_name'] = response.xpath('//div[@class="job-name"]/span/text()')[0].extract()
        item['advantage'] = response.xpath('//dd[@class="job-advantage"]/p/text()')[0].extract()
        # 这个字段要遍历处理
        item['job_description '] = response.xpath('//dd[@class="job_bt"]/div//p/text()').extract()
        # work_addr 和detail_addr拼接成完整的
        item['work_addr'] = response.xpath('//dd[@class="job-address clearfix"]/div[@class="work_addr"]/a/text()').extract()
        item['detail_addr'] = response.xpath('//dd[@class="job-address clearfix"]/div[@class="work_addr"]/text()').extract()
        # job_request = Field()  共五项 遍历分开储存
        item['job_request'] = response.xpath('//dd[@class="job_request"]/p/span/text()').extract()
        # 工作标签
        item['job_lable'] = response.xpath('//ul[@class="position-label clearfix"]/li/text()').extract()
        # 公司名称 全名 招聘的部门 相关信息（网址 行业 投资）
        item['company_name'] = response.xpath('//dl[@class="job_company"]/dt/a/img/@alt').extract()
        item['company_full_name'] = response.xpath('//dl[@class="job_company"]/dt/a/div/h2/text()').extract()
        item['company_concern'] = response.xpath('//ul[@class="c_feature"]/li/text()').extract()
        item['company_department'] = response.xpath('//div[@class="company"]/text()').extract()

        yield item

    def get_next_page(self):
        self.driver.find_elements_by_xpath('//span[text()="下一页"]').click()

