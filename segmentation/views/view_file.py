# -*- coding: utf-8 -*- 
# @File view_file.py
# @Time 2020/7/28 14:18
# @Author wcy
# @Software: PyCharm
# @Site
import os

import cv2
from flask import request, send_from_directory, jsonify, Blueprint, redirect, url_for

from config import SEGMENTATION_PATH
from segmentation.common.logger_config import logger
from segmentation.common.util import flask_content_type, check_param, load_image
from segmentation.server.dress_mask import save_segmentation, predict_segmentation

segmentation = Blueprint("segmentation", __name__, url_prefix="/segmentation")


@segmentation.route('/get_segmentation', methods=['get'])
def get_segmentation():
    # 下载文件接口
    try:
        fname = request.values.get('fname', None)
        if not fname is None:  # 判断是否是一个文件
            # 返回要下载的文件
            temp_file = os.path.join(SEGMENTATION_PATH, fname)
            if os.path.exists(temp_file):
                name, path = os.path.basename(temp_file), os.path.dirname(temp_file)
                # return send_file(ftp.send_wav_file(filename), mimetype="audio/wav", attachment_filename=filename)
                return send_from_directory(path, name, as_attachment=True)
        return jsonify({"msg": "文件不存在!"})
    except Exception as e:
        logger.error(f"接口异常{e}")
        return jsonify({"msg": "文件不存在!"})


@segmentation.route("/predict", methods=["GET", "POST"])
def predict():
    try:
        datas = flask_content_type(request)
        # 检查参数
        success = check_param(["image_url"], datas)
        if not success:
            return jsonify(code=4, msg="缺失必须的参数")
        # 获取图片url
        image_url = datas.get("image_url", "")
        if image_url == "":
            return jsonify(code=1, msg=f"image_url:{image_url} does not exist")
        image = load_image(image_url)
        if image is None:
            return jsonify(code=2, msg=f"Image invalid format")
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        if image.shape[2] == 4:
            image = image[..., :3]
        segmentation = predict_segmentation(image)
        file_name = save_segmentation(segmentation, image)
        url = f"http://222.85.230.14:12347/segmentation/get_segmentation?fname={file_name}"
        return jsonify(code=0, data={"url": url}, msg=f"ok")
        # print(url_for('segmentation.get_segmentation', fname=file_name))
        # return redirect(url_for('segmentation.get_segmentation', fname=file_name))
    except Exception as e:
        logger.error(f"{e}")
        return jsonify(code=500, msg=f"未知错误")
