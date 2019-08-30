#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : test_json.py
@Author: JACK
@Date  : 2019/8/29
@Des   :
"""
import json

json_path = "E:\jackstudy\LetApiRun\data\Dface\菜单管理\\test_searchall.json"
json_path_2 = "E:\jackstudy\LetApiRun\data\Dface\\test_login_1.json"

a = json.load(json_path)
print(a)



b = open(json_path_2)
print(b)
b.read()
print(b)
# b.read()
# print(dict(b))
