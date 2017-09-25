
import re
import time
import os
base_dir = os.path.dirname(os.path.abspath(__file__))

import requests
from datetime import datetime

from TaobaoShop import TaoBao


def find_vidoe_url(url):
    response = requests.get(url)
    code = response.encoding
    html = response.text
    if '//cloud.video.taobao.com' in html:
        return re.findall('"//cloud.video.taobao.com/.*?"', html)

    return None

def main():
    key_word = input("Key Word: ")
    speed = input("Speed: ")
    print("获取到关键字 {}".format(key_word))

    total_page = TaoBao(key_word).total_page
    print("获取到页面，共有 {} 页".format(total_page))

    shop_list_title = [
        'uid', '标题', '省份', '店铺url', '图标url', '主营项目', '视频url'
    ]

    now_time = datetime.now()
    now = datetime.strftime(now_time, "%Y-%m-%d %H_%M")
    file = open(os.path.join(base_dir,
                "{} {}.csv".format(key_word, str(now))), 'w', encoding="utf-8")
    for i in shop_list_title:
        try:
            file.write(i + ',')
        except UnicodeEncodeError as e:
            i = i.encode("GBK").decode("UTF-8")
            file.write(i + ',')
    file.write('\t\n')

    for page in range(total_page):
        total_tabao = TaoBao(key_word, page+1)
        print("============ 开始收集第 {} 页 ===========".format(page+1))

        shop_list = total_tabao.shop_list

        for shop in shop_list:
            total_list = [
                shop.get('uid'),
                shop.get('title'),
                shop.get('provcity'),
                "https:" + shop.get('shopUrl'),
                "https:" + shop.get('picUrl'),
                shop.get('mainAuction')
            ]

            video_url = find_vidoe_url("https:" + shop.get('shopUrl'))
            time.sleep(int(speed))

            add_url = "No Url"
            if video_url:
                add_url = video_url

            total_list.append(str(add_url))

            print(total_list[:-3])

            for i in total_list:
                if i is None:
                    i = ""
                try:
                    file.write(i + ',')
                except UnicodeEncodeError as e:
                    i = i.encode("GBK").decode("UTF-8")
                    file.write(i + ',')
            file.write('\t\n')

if __name__ == '__main__':
    main()












