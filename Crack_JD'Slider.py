from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import cv2
import time
from urllib import request

user = ''
passwd = ''


class CrackSlider:
    def __init__(self):
        self.url = 'https://passport.jd.com/new/login.aspx'  # 'https://www.geetest.com/Sensebot'
        self.option = Options()
        # self.option.add_argument('--headless')
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 20)
        self.user = user
        self.passwd = passwd

    def __del__(self):
        self.driver.quit()

    def parse(self):
        js = 'var q=Document.DocumentElement.scrollTop=3500'
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath('//div[@class="experience-box"]/div[@class="box-left"]/ul/li[2]').click()
        self.driver.find_element_by_xpath('//span[@class="geetest_wait_dot geetest_dot_1"]').click()

    def get_login(self):
        self.driver.get(self.url)
        locator = (By.LINK_TEXT, '账户登录')
        WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located(locator))
        self.driver.find_element_by_link_text('账户登录').click()
        time.sleep(1.5)
        self.driver.find_element_by_xpath('//input[@id="loginname"]').clear()
        self.driver.find_element_by_xpath('//input[@id="loginname"]').send_keys(self.user)
        time.sleep(0.8)
        self.driver.find_element_by_xpath('//input[@id="nloginpwd"]').send_keys(self.passwd)
        time.sleep(1.3)
        self.driver.find_element_by_xpath('//a[@id="loginsubmit"]').click()

        locator = (By.CLASS_NAME, 'JDJRV-smallimg')
        while 'pass' in self.driver.current_url:
            self.get_image_position()
            WebDriverWait(self.driver, 5, 0.3).until(EC.presence_of_element_located(locator))

    # 获取图形验证的图片，并滑动滑块实现滑块验证处理
    def get_image_position(self):
        # 获取滑块图片的下载地址
        src1 = self.driver.find_element_by_class_name('JDJRV-smallimg').find_element_by_xpath('img').get_attribute('src')
        # 获取背景大图图片的下载地址
        src2 = self.driver.find_element_by_class_name('JDJRV-bigimg').find_element_by_xpath('img').get_attribute('src')
        # print("image1:", image1)
        # print("image2:", image2)
        if src1 is None or src2 is None:
            return

        if self.driver.find_element_by_class_name('JDJRV-smallimg').is_displayed() is False:
            return

        image1_name = 'slide_block.png'  # 滑块图片名
        image2_name = 'slide_bkg.png'  # 背景大图名

        # 下载滑块图片并存储到本地
        request.urlretrieve(src1, image1_name)
        # 下载背景大图并存储到本地
        request.urlretrieve(src2, image2_name)

        # 获取图片，并灰化
        block = cv2.imread(image1_name, 0)
        template = cv2.imread(image2_name, 0)

        # 二值化之后的图片名称
        block_name = 'block.jpg'
        template_name = 'template.jpg'
        # 将二值化后的图片进行保存
        cv2.imwrite(template_name, template)
        cv2.imwrite(block_name, block)
        block = cv2.imread(block_name)
        block = cv2.cvtColor(block, cv2.COLOR_BGR2GRAY)
        block = abs(255 - block)
        cv2.imwrite(block_name, block)

        block = cv2.imread(block_name)
        template = cv2.imread(template_name)

        # 获取偏移量
        result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)
        # 查找block图片在template中的匹配位置，result是一个矩阵，返回每个点的匹配结果
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("min_val", min_val, "max_val", max_val, "min_loc", min_loc, "max_loc", max_loc)

        x, y = np.unravel_index(result.argmax(), result.shape)
        print("x,y:", x, y, 'result.shape:', result.shape)

        # 获取滑块
        element = self.driver.find_element_by_class_name('JDJRV-slide-inner.JDJRV-slide-btn')
        # 滑动滑块
        ActionChains(self.driver).click_and_hold(on_element=element).perform()

        y = int(y) + 3  # 矫正
        # 运动轨迹
        track = []
        track.append(int(7/8 * y))
        track.append(int(1/8 * y))
        for x in track:
            ActionChains(self.driver).move_to_element_with_offset(to_element=element, xoffset=x, yoffset=0).perform()
        # sleep(1)
        ActionChains(self.driver).release(on_element=element).perform()
        time.sleep(2)


if __name__ == "__main__":
    spider = CrackSlider()
    try:
        spider.get_login()
    except Exception as e:
        print(e)
