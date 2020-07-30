# -*- coding: utf-8 -*- 
# @Time 2020/7/8 10:30
# @Author wcy
import os


def run():
    command = "pip freeze > requirements.txt"
    os.system(command)


if __name__ == '__main__':
    run()