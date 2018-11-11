from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from lxml import etree
import time
from datetime import datetime
import codecs
import json
import random


class ITjuzi:
    """
    IT桔子爬虫 爬取117699家公司获投情况
    """
    def __init__(self):
        # self.option = webdriver.FirefoxOptions
        # self.option.add_argument('--headless')
        self.driver = webdriver.Firefox()
        self.file = codecs.open('ITjuzi.json', 'a', encoding='utf-8')
        self.items = []

    def __del__(self):
        self.driver.quit()
        self.file.close()

    def run(self):
        self.driver.get('https://www.itjuzi.com/company')

        self.driver.find_element_by_link_text('请登录').click()
        time.sleep(3)
        self.driver.find_elements_by_xpath('//input[@name="account"]')[0].send_keys('18550085462')
        time.sleep(0.5)
        self.driver.find_elements_by_xpath('//input[@name="password"]')[0].send_keys('usepython1314')
        time.sleep(0.5)
        self.driver.find_elements_by_xpath('//button[contains(@class,"submit")]')[0].click()
        time.sleep(8)

        i = 0
        js = 'var q=document.documentElement.scrollTop=150000'
        while True:
            # 开始处理 爬取数据
            self.driver.execute_script(js)
            self.parse()
            if self.parse() == 'Finished':
                return 'Done'
            self.next_page()
            i += 1
            num = random.choice(range(6, 10))

            if i % num == 0:
                time.sleep(random.choice(range(10, 20)))
            else:
                time.sleep(2)

    def parse(self):
        html = self.driver.page_source
        if html.find('page-item disabled') == -1:
            return 'Finished'
        xml = etree.HTML(html)
        # 提取字段
        root = xml.xpath('//div[@id="table"]/table/tbody/tr')

        for each in root:
            item = {}
            # 企业名
            item['company_name'] = each.xpath('./td[@class="_left namelink"]/span/text()')[0]
            # 简介
            item['summary'] = each.xpath('./td[@class="_left namelink"]/div[@class="onehang"]/text()')[0]
            # 行业
            item['industry'] = each.xpath('./td[3]/text()')[0]
            # 轮次
            item['investment_round'] = each.xpath('./td[4]/text()')[0]
            # 融资总额
            item['total_financing'] = each.xpath('./td[5]/text()')[0]
            # print(item)
            self.write(item)

            self.items.append(item)

    def next_page(self):
        # 下一页
        self.driver.find_element_by_xpath('//a[@aria-label="Goto next page"]').click()

    def write(self, item):
        content = '\n' + json.dumps(item, ensure_ascii=False)
        print(content)
        self.file.write(content)


if __name__ == "__main__":
    spider = ITjuzi()
    # start = int(input('请输入起始页: '))
    # end = int(input('请输入终止页: '))
    spider.run()

