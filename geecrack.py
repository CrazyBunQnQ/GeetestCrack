# coding:utf-8

# 等待时间
import time
# 产生随机数
import random
# 图片转换
import base64
# 图像处理标准库
from PIL import Image
# 鼠标操作
from selenium.webdriver.common.action_chains import ActionChains

# 初始偏移量
initial_offset = 39


def save_base64img(data_str, save_name):
    """
    将 base64 数据转化为图片保存到指定位置
    :param data_str: base64 数据，不包含类型
    :param save_name: 保存的全路径
    """
    img_data = base64.b64decode(data_str)
    file = open(save_name, 'wb')
    file.write(img_data)
    file.close()


def get_base64_by_canvas(driver, class_name, contain_type):
    """
    将 canvas 标签内容转换为 base64 数据
    :param driver: webdriver 对象
    :param class_name: canvas 标签的类名
    :param contain_type: 返回的数据是否包含类型
    :return: base64 数据
    """
    # 防止图片未加载完就下载一张空图
    bg_img = ''
    while len(bg_img) < 5000:
        getImgJS = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/png");'
        bg_img = driver.execute_script(getImgJS)
        time.sleep(0.5)
    # print(bg_img)
    if contain_type:
        return bg_img
    else:
        return bg_img[bg_img.find(',') + 1:]


def save_bg(driver, bg_path="bg.png", bg_class='geetest_canvas_bg geetest_absolute'):
    """
    保存包含缺口的背景图
    :param driver: webdriver 对象
    :param bg_path: 保存路径
    :param bg_class: 背景图的 class 属性
    :return: 保存路径
    """
    bg_img_data = get_base64_by_canvas(driver, bg_class, False)
    save_base64img(bg_img_data, bg_path)
    return bg_path


def save_full_bg(driver, full_bg_path="fbg.png", full_bg_class='geetest_canvas_fullbg geetest_fade geetest_absolute'):
    """
    保存完整的的背景图
    :param driver: webdriver 对象
    :param full_bg_path: 保存路径
    :param full_bg_class: 完整背景图的 class 属性
    :return: 保存路径
    """
    bg_img_data = get_base64_by_canvas(driver, full_bg_class, False)
    save_base64img(bg_img_data, full_bg_path)
    return full_bg_path


def get_slider(driver, slider_class='geetest_slider_button'):
    """
    获取滑块
    :param slider_class: 滑块的 class 属性
    :return: 滑块对象
    """
    while True:
        try:
            slider = driver.find_element_by_class_name(slider_class)
            break
        except:
            time.sleep(0.5)
    return slider


def is_pixel_equal(img1, img2, x, y):
    """
    判断两个像素是否相同
    :param image1: 图片1
    :param image2: 图片2
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    """
    # 取两个图片的像素点
    pix1 = img1.load()[x, y]
    pix2 = img2.load()[x, y]
    threshold = 60
    if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(
            pix1[2] - pix2[2] < threshold)):
        return True
    else:
        return False


def get_offset(full_bg_path, bg_path):
    """
    获取缺口偏移量
    :param full_bg_path: 不带缺口图片路径
    :param bg_path: 带缺口图片路径
    :return:
    """
    full_bg = Image.open(full_bg_path)
    bg = Image.open(bg_path)
    left = initial_offset
    for i in range(left, full_bg.size[0]):
        for j in range(full_bg.size[1]):
            if not is_pixel_equal(full_bg, bg, i, j):
                left = i
                return left
    return left


def get_track(distance):
    """
    根据偏移量获取拟人的移动轨迹
    :param distance: 偏移量
    :return: 移动轨迹
    """
    track = []
    current = 0
    mid = distance * 3 / 4
    t = random.randint(2, 3) / 10
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


def drag_the_ball(driver, track):
    """
    根据运动轨迹拖拽
    :param driver: webdriver 对象
    :param track: 运动轨迹
    """
    slider = get_slider(driver)
    ActionChains(driver).click_and_hold(slider).perform()
    while track:
        x = random.choice(track)
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
        track.remove(x)
    time.sleep(0.1)
    # 模拟人往回滑动
    imitate = ActionChains(driver).move_by_offset(xoffset=-1, yoffset=0)
    time.sleep(0.015)
    imitate.perform()
    time.sleep(random.randint(6, 10) / 10)
    imitate.perform()
    time.sleep(0.04)
    imitate.perform()
    time.sleep(0.012)
    imitate.perform()
    time.sleep(0.019)
    imitate.perform()
    time.sleep(0.033)
    ActionChains(driver).move_by_offset(xoffset=1, yoffset=0).perform()
    # 放开圆球
    ActionChains(driver).pause(random.randint(6, 14) / 10).release(slider).perform()
