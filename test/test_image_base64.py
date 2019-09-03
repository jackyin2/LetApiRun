#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : test_image_base64.py
@Author: JACK
@Date  : 2019/8/29
@Des   :
"""
import base64
import os

ImagePath = "E:\\jackstudy\\LetApiRun\\test_image"


for i in os.listdir(ImagePath):
    with open(os.path.join(ImagePath, i), "rb") as f:
        base64_data = base64.b64encode(f.read())
        base64_data = str(base64_data, encoding="utf-8")
        print(base64_data)
from let_utils import image_2_base64

a = eval("image_2_base64('E:\jackstudy\LetApiRun\test_image\3gi9schig3ahots0.jpg')")