from selenium import webdriver
import time
from datetime import datetime


def main():
    driver = webdriver.Firefox()
    # 登陆页面
    driver.get('https://passport.jd.com/new/login.aspx')
    time.sleep(3)
    driver.find_element_by_link_text('账户登录').click()
    # 填写用户名和密码
    driver.find_element_by_id('loginname').send_keys('18550085462')
    time.sleep(1)
    driver.find_element_by_id('nloginpwd').send_keys('Wjiaming.')
    time.sleep(1)
    driver.find_element_by_id('loginsubmit').click()
    time.sleep(10)
    # 然后会有滑动验证码 目前是人工滑动

    # 登陆后去相应页面去抢购
    driver.get('https://item.jd.com/8535863.html')
    # 找到抢购的按钮 判断是否可以抢购

    # 10月25日10:00开抢
    stime = datetime.datetime(2018,10,25,10,0,0)
    while True:
        now = datetime.now()
        if now > stime:
            break
        else:
            pass

    while True:
        # 选择极光蓝
        driver.find_element_by_xpath('//a[contains(@clstag, "极光蓝")]').click()
        # 选择运行内存大小和存储
        driver.find_element_by_xpath('//a[contains(@clstag, "8GB+128GB")]').click()
        # 点击抢购按钮
        driver.find_element_by_xpath('//a[@id="choose-btn-ko"]').click()
        # 前往购物车
        # driver.find_element_by_id('GotoShoppingCart').click()
        try:
            href = driver.find_element_by_xpath('//a[@id="choose-btn-ko"]').get_attribute('href')
        except Exception:
            href = '123'
        if href.endswith('#none'):
            driver.refresh()
        else:
            break
    try:
        # 选择极光蓝
        driver.find_element_by_xpath('//a[contains(@clstag, "极光蓝")]').click()
        # 选择运行内存大小和存储
        driver.find_element_by_xpath('//a[contains(@clstag, "8GB+128GB")]').click()
        # 点击抢购按钮
        driver.find_element_by_xpath('//a[@id="choose-btn-ko"]').click()
    except Exception:
        pass
    # 抢购后会进入订单结算页 和购物车不同 这里直接提交订单
    # 基本信息 jd都默认帮你填好了 只要提交订单即可
    # 收货人信息 支付和配送方式 发票信息都要点一下保存
    # 收货人信息要先点 支付和配送方式的保存按钮才会出现
    try:
        driver.find_element_by_xpath('//a[contains(@onclick, "save_Consignee")]').click()
        time.sleep(0.5)
    except Exception:
        pass
    try:
        driver.find_element_by_xpath('//a[contains(@onclick,"save_Payment")]').click()
        time.sleep(0.2)
    except Exception:
        pass
    try:
        driver.find_element_by_xpath('//a[contains(@onclick,"save_Invoice")]').click()
        time.sleep(0.2)
    except Exception:
        pass
    driver.find_element_by_id('order-submit').click()
    # 功能完成　其中可以自定义想要的颜色和内存大小什么的

    # # 前往购物车
    # driver.find_element_by_id('GotoShoppingCart').click()
    # # 出现了一个新页面 要切换到新页面
    # windows = driver.window_handles
    # driver.switch_to.window(windows[-1])
    # # 点击去结算
    # driver.find_element_by_class_name('submit-btn').click()
    # # 进入订单页面
    # driver.find_element_by_id('order-submit').click()
    # # 进入支付页面 切换微信支付 需要付钱了
    # driver.find_element_by_id('weixin').click()


if __name__ == "__main__":
    main()
    # 基本上功能都全 需要人工的有登陆的滑动验证码 和 最终支付的操作
    # driver之间的操作加入time.sleep(1) 休眠 以免太快 被封
    # 设置抢购时间，比如魅族16th 2018.10.25的10:00开始抢购，设置为到那个时间点 刷新
    # 疯狂点击抢购按钮 然后下单付款

