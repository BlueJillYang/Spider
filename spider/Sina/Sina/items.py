# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # define the fields for your item here like:

    # 所有大类的标题和url
    parent_title = scrapy.Field()
    parent_url = scrapy.Field()

    # 所有小类的标题和url
    sub_title = scrapy.Field()
    sub_url = scrapy.Field()

    # 小类目录存储路径
    sub_filename = scrapy.Field()

    # 子链接的标题，内容，url
    son_title = scrapy.Field()
    son_content = scrapy.Field()
    son_url = scrapy.Field()
