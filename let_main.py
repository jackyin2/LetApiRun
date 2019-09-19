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

# if __name__ == "__main__":
#     # 1 idel执行
#     main(path="E:\jackstudy\LetApiRun\data\custemor")
# #

