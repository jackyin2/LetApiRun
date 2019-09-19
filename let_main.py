#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_main.py
@Author: JACK
@Date  : 2019/8/23
@Des   :
"""
from let_runner import Runner
from let_result import HtmlReportor, TextReportor
from let_utils import is_path, is_file, is_dir


def main(path=None, file=None, init_conf=1, report_name=None):
    """
    执行流， 负责api的执行和报告的生成，还有邮件的分发
    :param path: 
    :param file: 
    :param init_conf: 默认加载配置
    :param report_name: 默认自动根据时间生成
    :return: 
    """
    runer = Runner(path=path, file=file, init_conf=init_conf)
    runer.run()
    # runer.report_to_ctr()
    report = HtmlReportor(report_name=report_name)
    report.report()


    # 结果生成


if __name__ == "__main__":
    # 1 idel执行
    main(path="E:\jackstudy\LetApiRun\data\custemor")

    # 2 命令行执行
    # import argparse
    #
    # parser = argparse.ArgumentParser(description="这是一款测试api的小框架，具有参数化，异常定位等特性")
    # parser.add_argument("-d", "--dir", help="测试目录", type=str)
    # parser.add_argument("-f", "--file", help="测试文件", type=str, default=None)
    # parser.add_argument("-c", "--conf", help="初始化配置文件,默认加载, 不加载设置为0", type=int, default=1)
    # parser.add_argument("-r", "--report", help="测试报告", type=str)
    # args = parser.parse_args()
    # print(is_file(args.file), args.file)
    # if not is_dir(args.dir):
    #     print("is not a true dir ,please check! ")
    #     exit(0)
    # elif not is_file(args.file):
    #     print("is not a true file ,please check! ")
    #     exit(0)
    # main(path=args.dir, file=args.file, init_conf=args.conf, report_name=args.report)
