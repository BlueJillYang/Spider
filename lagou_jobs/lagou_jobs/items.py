# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class LagouJobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = Field()
    advantage = Field()
    job_description = Field()
    # work_addr 和detail_addr拼接成完整的
    work_addr = Field()
    detail_addr = Field()
    # job_request = Field()  共五项 遍历分开储存
    job_request = Field()
    # 工作标签
    job_label = Field()
    # 公司名称 全名 招聘的部门 相关信息（网址 行业 投资）
    company_name = Field()
    company_full_name = Field()
    company_concern = Field()
    company_department = Field()


