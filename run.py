# -*- coding: utf-8 -*- 
# @File run.py
# @Time 2020/7/28 14:50
# @Author wcy
# @Software: PyCharm
# @Site
from flask import Flask

from segmentation.views.view_file import segmentation

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(segmentation)


@app.before_first_request
def before():
    global module
    # 初始化模型


if __name__=='__main__':
  app.run(host="0.0.0.0", port=5050)