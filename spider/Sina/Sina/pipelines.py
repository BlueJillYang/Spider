# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs


class SinaPipeline(object):
    def process_item(self, item, spider):
        sonUrls = item['son_url']

        # 文件名为子链接url中间部分，并将 / 替换为 _，保存为 .txt格式
        filename = sonUrls[7:-6].replace('/', '_')
        filename += ".txt"

        fp = codecs.open(item['sub_filename']+'/'+filename, 'w', encoding='utf-8')
        fp.write(item['son_content'])
        fp.close()

        return item
