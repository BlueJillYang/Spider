from urllib import parse, request
import requests
from lxml import etree
import os


class Tieba:
    def __init__(self):
        self.url = 'https://tieba.baidu.com/f?'

        self.headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"}
        self.folder = os.getcwd() + '/tieba_Images'
        self.links = []
        if not os.path.isdir(self.folder):
            os.makedirs(self.folder)

    def loadPage(self, key, page):
        """
        读取页面源代码提取帖子的links
        :param key: 贴吧名
        :param page: 第几页
        :return:
        """
        page = (int(page)-1) * 50
        url = self.url + key + '&pn={}'.format(page)
        response = requests.get(url, headers=self.headers)
        print('正在请求{}'.format(url))
        print(response)
        html = etree.HTML(response.content)

        links = html.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        print(links)
        self.loadPost(links)

    def loadPost(self, links):
        url = 'https://tieba.baidu.com{}'
        for link in links:
            response = requests.get(url.format(link), headers=self.headers)
            html = etree.HTML(response.content)
            link_lists = html.xpath('//div[@class="post_bubble_middle"]')
            self.links.extend(link_lists)

    def loadImages(self):
        """
        读取帖子中所有的图片
        :param link: 帖子的链接
        :return:
        """
        print('正在爬帖子中图片')
        for link in self.links:
            image_name = link.split('/')[-1]
            image = requests.get(link).content
            self.writeImages(image, image_name)

    def writeImages(self, image, image_name):
        """
        写入图片
        :param image: 图片bytes
        :param image_name: 图片名
        :return:
        """
        image_name = self.folder + '/{}'.format(image_name)
        print('正在写入{}'.format(image_name))
        with open(image_name, 'w') as f:
            f.write(image)

    def run(self, key, beginPage, endPage):
        """
        总调度器
        :param key: 贴吧名
        :param beginPage: 开始页码
        :param endPage: 终止页码
        :return:
        """
        for i in range(beginPage, endPage+1):
            self.loadPage(key, i)

        self.loadImages()


if __name__ == "__main__":
    kw = input("请输入需要爬取的贴吧名:")
    beginPage = int(input("请输入起始页："))
    endPage = int(input("请输入结束页："))

    key = parse.urlencode({"kw": kw})
    print(key)
    spider = Tieba()
    spider.run(key, beginPage, endPage)
