# -*- coding: utf-8 -*-
import scrapy
import os
from ..items import SinaItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    # allowed_domains = ['http://news.sina.com.cn/guide/']
    start_urls = ['http://news.sina.com.cn/guide/']
    path = 'Data/'

    def parse(self, response):
        # items=[] 存储item
        items = []
        # 用xpath取出response中的所有大类和小类
        # 大类的标题和url
        parent_titles = response.xpath('//div[@id="tab01"]/div/h3/a/text()').extract()
        parent_urls = response.xpath('//div[@id="tab01"]/div/h3/a/@href').extract()

        # 所有小类的标题和url
        sub_titles = response.xpath('//div[@id="tab01"]/div/ul/li/a/text()').extract()
        sub_urls = response.xpath('//div[@id="tab01"]/div/ul/li/a/@href').extract()

        # 例如大类的url开头是news.sina... 其下的小类开头也是news.sina../subs(不同) 判断是否为其子
        for i in range(0, len(parent_titles)):
            newpath = self.path + parent_titles[i] + '/'
            # 如果目录不存在，则创建目录
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            for j in range(0, len(sub_titles)):
                # 实例化item
                item = SinaItem()

                item['parent_url'] = parent_urls[i]
                item['parent_title'] = parent_titles[i]

                # belong布尔类型判断大小类归属
                belong = sub_urls[j].startswith(parent_urls[i])

                if belong:
                    new_path = newpath + sub_titles[j] + '/'
                    # 创建目录
                    if not os.path.exists(new_path):
                        os.makedirs(new_path)

                    item['sub_url'] = sub_urls[j]
                    item['sub_title'] = sub_titles[j]
                    item['sub_filename'] = new_path

                    items.append(item)

        for item in items:
            print('No.1', item)
            yield scrapy.Request(url=item['sub_url'], meta={'meta1': item}, callback=self.parse_items)

    def parse_items(self, response):
        # 取出meta数据
        meta1 = response.meta['meta1']

        items = []

        # 取出小类页面里的所有.shtml超链接
        href_list = response.xpath('//a/@href').extract()

        for i in range(0, len(href_list)):
            belong = href_list[i].startswith(meta1['parent_url']) and href_list[i].endswith('.shtml')

            if belong:
                item = SinaItem()
                item['parent_title'] = meta1['parent_title']
                item['parent_url'] = meta1['parent_url']
                item['sub_title'] = meta1['sub_title']
                item['sub_url'] = meta1['sub_url']
                item['sub_filename'] = meta1['sub_filename']
                item['son_url'] = href_list[i]

                items.append(item)
        for item in items:
            print('No2', item)
            yield scrapy.Request(url=item['son_url'], meta={'meta2': item}, callback=self.final_parse)

    def final_parse(self, response):
        item = response.meta['meta2']
        content = ""
        head = response.xpath('//h1[@class="main-title"]/text()').extract()
        content_list = response.xpath('//div[@class="article"]/p/text()').extract()

        # 将p标签里的文本内容合并到一起
        for content_one in content_list:
            content += content_one

        item['son_title'] = head
        item['son_content'] = content

        print('No3', item)
        yield item




