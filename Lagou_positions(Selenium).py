from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from lxml import etree
import time
import codecs
import json
import csv


class LagouSpider:
    def __init__(self):
        self.items = []
        self.option = Options()
        self.option.add_argument('--headless')
        self.driver = webdriver.Firefox()
        self.url = 'http://www.lagou.com/jobs/list_python?px=default&city=%E8%8B%8F%E5%B7%9E'
        self.filename = 'lagou_positions.csv'
        self.file = codecs.open(self.filename, 'a', encoding='utf-8')
        self.headers = 1
        self.fieldnames = ['job_name', 'job_addr', 'salary', 'job_request', 'company_name', 'industry', 'advantage', 'href', 'labels']
        self.csvfile = csv.DictWriter(self.file, fieldnames=self.fieldnames)

    def __del__(self):
        self.file.close()
        self.driver.quit()

    def parse(self):
        # 进入目标页面
        self.driver.get(self.url)
        response = self.driver.page_source

        # etree转换 找到职位链接
        xml = etree.HTML(response)
        self.parse_list(xml)
        # 得到url列表
        position_links = xml.xpath('//a[@class="position_link"]/@href')

        if_next_page = response.find('pager_next_disabled')
        print(if_next_page)

        time.sleep(1)
        while True:
            # 先将所有目标岗位的单独url存到列表中
            if if_next_page == -1:
                self.driver.find_elements_by_xpath('//span[text()="下一页"]')[0].click()
                response = self.driver.page_source

                # etree转换 找到职位链接
                xml = etree.HTML(response)
                self.parse_list(xml)
                # 将url添加到列表中
                position_links += xml.xpath('//a[@class="position_link"]/@href')

                if_next_page = response.find('pager_next_disabled')
                time.sleep(2)
            else:
                break
        # print(position_links)
        # print(len(position_links))
        # self.parse_detail(self.items)

    def parse_list(self, response):
        items = self.items
        root = response.xpath('//li[contains(@class,"con_list_item")]')
        for each in root:
            item = {}
            item['job_name'] = each.xpath('.//a/h3/text()')[0]
            item['job_addr'] = each.xpath('.//a/span/em/text()')[0]
            item['salary'] = each.xpath('.//span[@class="money"]/text()')[0]
            item['job_request'] = ''.join(each.xpath('.//div[@class="p_bot"]/div/text()'))
            item['company_name'] = each.xpath('.//div[@class="company"]/div/a/text()')[0]
            item['industry'] = each.xpath('.//div[@class="company"]/div[@class="industry"]/text()')[0]
            item['advantage'] = each.xpath('.//div[@class="list_item_bot"]/div[@class="li_b_r"]/text()')[0]
            item['href'] = each.xpath('.//a[@class="position_link"]/@href')[0]
            if len(each.xpath('.//div[@class="list_item_bot"]/div/span/text()')) != 0:
                item['labels'] = each.xpath('.//div[@class="list_item_bot"]/div/span/text()')[0]

            self.parse_csv(item)
            items.append(item)
        # print(items)
        # print('len: {}'.format(len(items)))

    def parse_csv(self, item):
        self.csvfile.writerow(item)

    def parse_detail_code(self, links):
        items = []
        file = codecs.open(self.filename, 'w', encoding='utf-8')
        for link in links:
            item = {}
            r = requests.get(url=link, headers=self.headers)
            response = etree.HTML(r.text)
            # item['job_name'] = response.xpath('//div[@class="job-name"]/span/text()')
            # item['advantage'] = response.xpath('//dd[@class="job-advantage"]/p/text()')
            # 这个字段要遍历处理
            item['job_description '] = response.xpath('//dd[@class="job_bt"]/div//p/text()')
            # work_addr 和detail_addr拼接成完整的
            item['work_addr'] = response.xpath('//dd[@class="job-address clearfix"]/div[@class="work_addr"]/a/text()')
            item['detail_addr'] = response.xpath('//dd[@class="job-address clearfix"]/div[@class="work_addr"]/text()')
            # job_request = Field()  共五项 遍历分开储存
            item['job_request'] = response.xpath('//dd[@class="job_request"]/p/span/text()')
            # 工作标签
            item['job_lable'] = response.xpath('//ul[@class="position-label clearfix"]/li/text()')
            # 公司名称 全名 招聘的部门 相关信息（网址 行业 投资）
            item['company_name'] = response.xpath('//dl[@class="job_company"]/dt/a/img/@alt')
            item['company_full_name'] = response.xpath('//dl[@class="job_company"]/dt/a/div/h2/text()')
            item['company_concern'] = response.xpath('//ul[@class="c_feature"]/li/text()')
            item['company_department'] = response.xpath('//div[@class="company"]/text()')
            print(item)

            items.append(item)

            content = json.dumps(dict(item), ensure_ascii=False) + '\n'
            file.write(content)

        file.close()
        print('写入完成')


if __name__ == '__main__':
    spider = LagouSpider()
    spider.parse()


