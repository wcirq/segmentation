# -*- coding: utf-8 -*- 
# @File    : __init__.py
# @Time 2020/7/28 10:24
# @Author wcy
# @Software: PyCharm
# @Site
from config import MODEL_FILE_PATH
from segmentation.model.yolact import Yolact

model = Yolact(input_size=550, fpn_channels=256, feature_map_size=[69, 35, 18, 9, 5], num_class=91, num_mask=32,
                   aspect_ratio=[1, 0.5, 2], scales=[24, 48, 96, 192, 384])
model.build(input_shape=(8, 550, 550, 3))
model.set_bn(mode="evel")
model.load_weights(MODEL_FILE_PATH)