# 模拟登陆北京大学软件工程moodle网站

import requests
from pyquery import PyQuery as pq
import time
from selenium import webdriver # 用于模拟浏览器
from PIL import Image
import pytesseract  # 用于识别验证码 

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Aoyou/OXF-eSxxVGVMIU8-KS51JGLArv5Of5uAJACh9ARxm03iXiYrW6nnQAzI"
header = {
    "origin": "http://124.207.24.134:8888",
    "Referer": "http://124.207.24.134:8888/apply/index",
    'User-Agent': userAgent,
}

def login(url):
    browser = webdriver.Chrome()
    browser.set_window_size(1920, 1080)
    browser.get(url)
    browser.save_screenshot('login.png')   # 截个屏

    # 定位
    verify = browser.find_element_by_xpath("/html/body/div[2]/div/form/div[3]/img")  # 定位验证码的位置
    verify_location = verify.location
    print(verify_location)
    verify_size = verify.size
    local = (verify_location['x'], verify_location['y'], verify_location['x'] + verify_size['width'], verify_location['y'] + verify_size['height'])

    pic = Image.open('login.png')
    pic = pic.crop(local)                 # 把验证码裁剪出来
    pic.save('login.png')
    verify_code = pytesseract.image_to_string(pic) # 识别验证码
    print(verify_code)

    print("开始模拟登录")
    account, password = "username", "******"  # 这里输入自己的用户名和密码
    elem = browser.find_element_by_xpath("/html/body/div[2]/div/form/div[1]/input")
    elem.send_keys(account)
    time.sleep(1)
    elem = browser.find_element_by_xpath("/html/body/div[2]/div/form/div[2]/input")
    elem.send_keys(password)
    time.sleep(1)
    elem = browser.find_element_by_xpath("/html/body/div[2]/div/form/div[3]/input")
    elem.send_keys(verify_code)
    time.sleep(1)
    elem = browser.find_element_by_xpath("/html/body/div[2]/div/form/div[4]")
    elem.click()
    return browser

if __name__ == "__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Aoyou/O19jWGEKRStEQ1g7ClI6YJWqdkrVfb-d1WtDMvmQfxhFQ7Kq6icGV59T",
        "Referer": "http://ss.pku.edu.cn/index.php/admission/admnotice",
        "Content-Type": "text/html; charset=utf-8"
    }
    url = f'http://124.207.24.134:8888/apply/index'

    result = login(url)
