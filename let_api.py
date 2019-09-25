#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : cmd.py.py
@Author: JACK
@Date  : 2019/9/19
@Des   :
"""
import argparse
from let_main import *
from let_utils import check_json


# 2 命令行执行
parser = argparse.ArgumentParser(description="这是一款测试api的小框架，具有参数化，异常定位等特性")
parser.add_argument("-d", "--dir", help="测试目录", type=str, required=True)
parser.add_argument("-f", "--file", help="测试文件", type=str, default=None)
parser.add_argument("-c", "--conf", help="初始化配置文件,默认加载, 不加载设置为0", type=int, default=1)
parser.add_argument("-r", "--report", help="测试报告", type=str)
parser.add_argument("-C", "--check", help="json文件检查", type=int, default=0)

args = parser.parse_args()
if not is_dir(args.dir):
    print("is not a true dir ,please check! ")
    exit(0)
elif not is_file(args.file):
    print("is not a true file ,please check! ")
    exit(0)
elif args.check == 1:
    check_json(args.dir)
    exit(0)
main(path=args.dir, file=args.file, init_conf=args.conf, report_name=args.report)