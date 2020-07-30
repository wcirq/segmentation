# -*- coding: utf-8 -*- 
# @Time 2020/7/3 12:42
# @Author wcy
import os
import platform

system = platform.system()

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
# 源码路径
SRC_PATH = os.path.join(BASE_DIR, "segmentation")
# 资源目录
RESOURCE_PATH = os.path.join(SRC_PATH, 'resources')
# 日志目录
LOGS_PATH = os.path.join(SRC_PATH, 'logs', 'info.log')
# 模型目录
MODEL_PATH = os.path.join(RESOURCE_PATH, 'model')
# 模型文件路径
MODEL_FILE_PATH = os.path.join(MODEL_PATH, 'weights_3.5164053.h5')
# segmentation目录
SEGMENTATION_PATH = os.path.join(RESOURCE_PATH, 'segmentation')
# tmp目录
TMP_PATH = os.path.join(RESOURCE_PATH, 'tmp')

# 数据路径
if system == "Linux":
    pass
else:
    pass
