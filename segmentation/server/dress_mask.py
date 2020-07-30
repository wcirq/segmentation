# -*- coding: utf-8 -*- 
# @File dress_mask.py
# @Time 2020/7/28 10:23
# @Author wcy
# @Software: PyCharm
# @Site
import os
import re
import cv2
import numpy as np
import tensorflow as tf
import uuid
from config import SEGMENTATION_PATH
from segmentation.server import model


def predict_segmentation(image):
    h, w, _ = image.shape
    image = cv2.resize(image, (550, 550))
    inputs = image.astype(np.float32)
    inputs = inputs[..., ::-1]
    inputs = np.expand_dims(inputs, axis=0)
    outputs = model(inputs)

    seg = outputs['seg']
    index = np.argmax(np.mean(np.reshape(tf.sigmoid(seg[0]).numpy(), (-1, 91)), axis=0))
    segmentation = tf.sigmoid(seg[0][..., index]).numpy()
    segmentation = cv2.resize(segmentation, (w, h))
    # print(index)
    ret, segmentation = cv2.threshold(segmentation, 0.05, 1, 0)
    return segmentation.astype(np.uint8)


def save_segmentation(mask, image):
    if mask.max() <= 2:
        mask = (mask*255).astype(np.uint8)
        mask = np.expand_dims(mask, axis=2)
    frame = np.concatenate((image, mask), axis=2)
    file_name = f'{re.sub("-", "", str(uuid.uuid4()))}.png'
    file_path = os.path.join(SEGMENTATION_PATH, file_name)
    cv2.cvtColor(mask, cv2.COLOR_RGBA2BGR)
    cv2.imwrite(file_path, frame)
    return file_name


if __name__ == '__main__':
    root = r"D:\2020.3.22款式图片\flower_photos\夹克_冲锋衣"
    file_list = os.listdir(root)
    for file in file_list[100:]:
        file_path = os.path.join(root, file)
        image = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        segmentation = predict_segmentation(image)
        save_segmentation(segmentation, image)

        # cv2.imshow("segmentation", segmentation)
        # ret, segmentation = cv2.threshold(segmentation, 0.05, 1, 0)
        # segmentation = np.expand_dims(segmentation, axis=2)
        # segmentation = np.tile(segmentation, [1, 1, 3])
        # segmentation = ((1 - segmentation) * 255).astype(np.uint8)
        # merge = cv2.addWeighted(image, 0.5, segmentation, 0.5, 0)
        # cv2.imshow("merge", merge)
        # # cv2.imshow("segmentation", segmentation)
        # # cv2.imshow("image", image)
        # cv2.waitKey(1)
