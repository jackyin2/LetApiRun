#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : test_let_loader.py
@Author: JACK
@Date  : 2019/8/24
@Des   :
"""
from let_loader import Loader


if __name__ == "__main__":
    a = Loader()
    a.load_cases_from_dir("E:\jackstudy\LetApiRun\data\Dface")
    for i in a:
        print(type(i["test_dir"]) is list)
        print(type(i))
        print()