# coding:utf-8
# 等待时间 产生随机数
import time
# Geettest 验证码
import geecrack
# web测试
from selenium import webdriver
# 鼠标操作
# 预期条件
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

username = ""
password = ""

driver = webdriver.Chrome()
driver.get("https://passport.bilibili.com/login")
wait = WebDriverWait(driver, 100)
wait.until(expected_conditions.presence_of_element_located((By.ID, 'login-username')))
wait.until(expected_conditions.presence_of_element_located((By.ID, 'login-passwd')))
input_user = driver.find_element_by_id('login-username')
input_pwd = driver.find_element_by_id('login-passwd')
submit_btn = driver.find_element_by_class_name('btn-login')
input_user.send_keys(username)
input_pwd.send_keys(password)
submit_btn.click()

# 加载 Geetest 验证码
wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_slice')))
wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_fullbg')))

# 保存包含缺口的页面截图
bg_path = geecrack.save_bg(driver)
# 保存完整背景图
full_bg_path = geecrack.save_full_bg(driver)
# 移动距离
distance = geecrack.get_offset(full_bg_path, bg_path)
# 获取移动轨迹
track = geecrack.get_track(distance)
# 滑动圆球至缺口处
geecrack.drag_the_ball(driver, track, offset=30)
# 到此就完成滑动验证码啦~
time.sleep(10)
driver.close()
