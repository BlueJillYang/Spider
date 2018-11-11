# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json


class LagouJobsPipeline(object):
    def __init__(self):
        self.filename = codecs.open('lagou.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.filename.write(json.dumps(item))
        return item

    def close_spiders(self, spider):
        self.filename.close()
