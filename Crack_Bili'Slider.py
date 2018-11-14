from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import re
import requests
import time
from io import BytesIO
import random


class BiliBili:
    def __init__(self):
        self.option = Options()
        self.option.add_argument('--headless')
        # self.driver = webdriver.Firefox(options=self.option)
        self.driver = webdriver.Firefox()
        self.url = 'https://passport.bilibili.com/login'
        self.wait = WebDriverWait(self.driver, 20)
        self.if_success = False

    def __del__(self):
        print('退出 关闭浏览器')
        self.driver.quit()

    def login(self, username, password):
        self.driver.get(self.url)
        # 等待页面加载完成后操作
        locator = (By.CLASS_NAME, 'gt_slider')
        try:
            WebDriverWait(self.driver, 15, 0.5).until(EC.presence_of_element_located(locator))
            # print('可执行操作')
        except Exception as e:
            print(e)

        # 写入用户名 密码
        self.driver.find_element_by_xpath('//li[@class="item username status-box"]/input').clear()
        self.driver.find_element_by_xpath('//li[@class="item username status-box"]/input').send_keys(username)
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//li[@class="item password status-box"]/input').send_keys(password)

        while not self.if_success:
            # 获取完整的图片
            full_image = self.get_image('gt_cut_fullbg_slice')

            # 获取带缺口的图片
            bg_image = self.get_image('gt_cut_bg_slice')

            # 获取对比后的缺口x坐标
            x_offset = self.get_position(full_image, bg_image)

            # 计算运动轨迹
            track = self.get_trace(x_offset)

            # 滑动按钮完成验证
            result = self.slide(track)

            if u'验证通过' in result:
                self.if_success = True
            elif u'出现错误:' in result:
                self.driver.execute_script('location.reload()')
            elif u'再' in result:
                time.sleep(4)
                continue
            elif u'吃' in result:
                time.sleep(5)
            else:
                break

    def draft_slider(self):
        # 鼠标悬停在滑块
        mouse = self.driver.find_element_by_xpath('//div[contains(@class, "gt_slider_knob")]')
        ActionChains(self.driver).move_to_element(mouse).perform()

    def get_image(self, class_name):
        """
        下载源码中的图片
        :param class_name: 需要查找的元素的class name
        :return: 返回处理好的图片
        """
        image_style = self.driver.find_elements_by_class_name(class_name)
        # print(image_style)
        # 如果没有这个元素 报错
        if len(image_style) == 0:
            return 'No Such a class'
        # 处理图片url
        src_style = image_style[0].get_attribute('style')
        # print(src_style)
        href = re.findall(r'url.+(https.+?)"', src_style)[0]
        print(href)
        if href.endswith('.webp'):
            href.replace('webp', 'jpg')

        image_name = href.rsplit('/')[-1]
        print(image_name)

        location_list = list()
        for image_obj in image_style:
            location = {}
            # print(image_obj.get_attribute('style'))
            coordinate = re.findall(r'background-position: (.*?\d+)px (.*?\d+)px;', image_obj.get_attribute('style'))
            # print(coordinate[0])
            location['x'] = int(coordinate[0][0])
            location['y'] = int(coordinate[0][1])
            # print(location)
            location_list.append(location)

        # requests 请求图片url地址 下载图片
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6776.400 QQBrowser/10.3.2577.400'}
        response = requests.get(url=href, headers=headers)
        image = Image.open(BytesIO(response.content))
        # image.show()

        image = self.reduce_image(image, location_list)
        return image

    def reduce_image(self, image, location_list):
        """
        还原被打乱的图片
        :param image: 原来被打乱的图片
        :param location_list: 坐标列表
        :return: 返回处理后的 正常可视的图片
        """
        new_img = Image.new('RGB', (260, 116))
        up_img_list = list()
        down_img_list = list()
        for location in location_list:
            if location['y'] == -58:
                up_img_list.append(image.crop((abs(location['x']), 58, abs(location['x']) + 10, 116)))
            if location['y'] == 0:
                down_img_list.append(image.crop((abs(location['x']), 0, abs(location['x']) + 10, 58)))

        x_offset = 0
        for img in up_img_list:
            new_img.paste(img, (x_offset, 0))
            x_offset += img.size[0]

        x_offset = 0
        for img in down_img_list:
            new_img.paste(img, (x_offset, 58))
            x_offset += img.size[0]
        new_img.show()
        return new_img

    def get_position(self, image1, image2):
        """
        比较两张图片 RGB色差超过50 就认为是缺口位置
        :param image1: 完整图片
        :param image2: 带缺口图片
        :return: x坐标位置
        """
        for x in range(260):
            for y in range(116):
                if not self.check_crack(image1, image2, x, y):
                    return x

    def check_crack(self, image1, image2, x, y):
        """
        判断image1, image2的[x, y]这一像素是否相似，如果该像素的RGB值相差都在50以内，则认为相似。
        :param image1: 完整图片
        :param image2: 带缺口图片
        :param x: x坐标
        :param y: y坐标
        :return: Boolean
        """
        pixel1 = image1.getpixel((x, y))
        pixel2 = image2.getpixel((x, y))
        for i in range(0, 3):
            if abs(pixel1[i] - pixel2[i]) >= 50:
                return False
        return True

    def get_trace(self, x):
        """
        计算运动轨迹 模拟自然行为
        :param x: 缺口x坐标
        :return:
        """
        print('正在计算滑动轨迹')
        print('x_offset: ', x)

        track = []
        distance = x
        distance = int(distance) - 4  # 矫正值
        exceed_distance = int(distance) + 20  # 模拟人类超出值
        print('缺口坐标', distance)
        fast_distance = distance * (7 / 8)
        track.append(int(fast_distance))
        track.append(distance-fast_distance)
        return track

    def slide(self, track):  # 模拟拖动滑块
        print('开始模拟')
        # 找寻滑块标签
        slider = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_slider_knob')))
        ActionChains(self.driver).click_and_hold(slider).perform()  # 执行
        print(track)
        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.2)
        ActionChains(self.driver).release().perform()  # 释放滑
        time.sleep(1)
        dom_div_gt_info = self.driver.find_element_by_class_name('gt_info_type')
        return dom_div_gt_info.text


if __name__ == "__main__":
    spider = BiliBili()
    spider.login('', '')

