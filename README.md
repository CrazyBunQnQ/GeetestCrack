# Python Selenium 破解滑块验证码最新版

>本文破解方式截止到 2018 年 9 月 2 日的 GEETEST 有效，本文不定期更新。

有爬虫，自然就有反爬虫，就像病毒和杀毒软件一样，有攻就有防，两者彼此推进发展。为了防止爬虫自动注册，批量生成垃圾账号，几乎所有网站的注册页面都会用到验证码技术。而目前市场占有率很高的反爬技术验证码就是 GEETEST 滑动验证码，本篇博客就是介绍如何破解 GEETEST 验证码。

![GEETEST 客户](http://wx1.sinaimg.cn/large/a6e9cb00ly1fuvm1s3u1bj21kw20xb29.jpg)

## 需要用到的库

```python
# 图像处理标准库
from PIL import Image   
# web测试
from selenium import webdriver
# 鼠标操作
from selenium.webdriver.common.action_chains import ActionChains
# 等待时间
import time
# 产生随机数
import random
# 图片转换
import base64
```

## 破解步骤

1. 利用 selenium 进入滑块验证码页面。（略：会 selenium 的都知道怎么打开页面吧）
2. [执行 JS 获取滑块背景图和完整背景图的数据。](#获取背景图数据)
3. [利用 base64 将图片数据转化为图片保存到本地。](#保存背景图)
4. [通过图片像素对比分析获取缺口位置与滑块移动距离。](#计算移动距离)
5. [机器模拟人工滑动轨迹。](#模拟人工滑动)

>参考了 [\_\_\_PANDA\_\_\_](https://blog.csdn.net/qq_38685503/article/details/81187105) 的文章，主要完善了下载背景图片步骤

### 获取背景图数据

通过 `get_base64_by_canvas(driver, class_name, contain_type)` 方法获取指定类名的 `canvas` 标签图片数据

### 保存背景图片

通过 `save_base64img(data_str, save_name)` 方法将图片 base64 数据转化为图片并保存到本地

>`save_bg()` 和 `save_full_bg()` 方法分别将这两步合在了一起

### 计算移动距离

`get_offset(full_bg_path, bg_path)` 方法，通过对比缺口背景图和完整背景图来判断缺口位置，从而计算出滑块需要滑动多少距离

### 模拟人工滑动

`get_track(distance)` 方法根据移动距离生成模拟人的移动轨迹，该方法直接借鉴 [\_\_\_PANDA\_\_\_](https://blog.csdn.net/qq_38685503/article/details/81187105) 的方法

至此，可以就可以不用提前保存各种验证码图片了，全都能自动破解验证码了~