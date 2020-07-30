# -*- coding: utf-8 -*- 
# @File util.py
# @Time 2020/7/28 14:23
# @Author wcy
# @Software: PyCharm
# @Site
import json
import os
import re
import uuid

import cv2
import numpy as np
import requests

from config import TMP_PATH


def flask_content_type(requests) -> dict:
    """根据不同的content_type来解析数据"""
    if requests.method == 'POST':
        if 'application/x-www-form-urlencoded' == requests.content_type:
            data = requests.form
        else:  # 无法被解析出来的数据
            if requests.data:
                data = json.loads(requests.data)
            else:
                raise Exception('无法解析')
    elif requests.method == 'GET':
        data = requests.args
    else:
        raise Exception('只支持GET和POST请求')
    return data


def check_param(params: list, datas: dict):
    """
    检查参数是否存在
    :param params: 必须包含的参数 list
    :param datas: 传入的参数
    :return: bool 是否通过
    """
    keys = list(datas.keys())
    result = set(params) <= set(keys)
    return result


def load_image(url):
    res = requests.get(url)
    if res.status_code == 200 and 'jpeg' in res.headers['content-type']:
        image_name = f'{re.sub("-", "", str(uuid.uuid4()))}.jpg'
        image_path = os.path.join(TMP_PATH, image_name)
        with open(image_path, 'wb') as fp:
            for chunk in res:
                fp.write(chunk)
        img_arr = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        return img_arr
    else:
        return None


if __name__ == '__main__':
    # load_image("https://res.gucci.cn/resources/2020/6/16/15922997452278407_ws_235X235.jpg")
    load_image("https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1595938026220&di=8a55cb171a01330bd5d12ba99e184b6f&imgtype=0&src=http%3A%2F%2Fgss0.baidu.com%2F9fo3dSag_xI4khGko9WTAnF6hhy%2Fzhidao%2Fpic%2Fitem%2Fa8014c086e061d95d8fb4c247bf40ad162d9ca69.jpg")