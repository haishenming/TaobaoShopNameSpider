import re
import json

import requests


class TaoBao:
    def __init__(self, key_word, page_num=1):
        self.key_word = key_word    # 关键字
        self.base_url = "https://shopsearch.taobao.com/search?app=shopsearch"  # 搜索页面的基本链接
        self.page_num = page_num   # 页码
        self.page_count = 20  # 页码商品基数

    @property
    def response(self):
        """ 搜索商铺
        """
        url = self.base_url + "&q=" + self.key_word + "&s=" + str((self.page_num - 1) * self.page_count)
        response = requests.get(url)

        return response

    @property
    def g_page_config(self):
        """ 解析response，获取url列表，商铺名称
        """

        self.text = self.response.text
        g_page_config = re.search('g_page_config = {.*?};', self.text).group(0)
        g_page_config = json.loads(g_page_config[15:-1])

        return g_page_config

    @property
    def shop_list(self):
        """ 获取店铺列表
            （uid, 店铺名称，昵称， 省份， 好评率， 店铺链接， 主营）
        """

        shop_info_dict = self.g_page_config["mods"]["shoplist"]["data"]["shopItems"]

        return shop_info_dict

    @property
    def total_page(self):
        """ 最大页码
        """
        return self.g_page_config["mods"]["pager"]["data"]["totalPage"]