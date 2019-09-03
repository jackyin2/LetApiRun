#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_main.py
@Author: JACK
@Date  : 2019/8/23
@Des   :
"""
from let_runner import Runner
from let_result import HtmlReportor


def main(path):
    runer = Runner(path=path)
    runer.run()
    # runer.report_to_ctr()
    report = HtmlReportor(report_name="report_template_2.html", type='html')
    report.report()

    # 结果生成

if __name__ == "__main__":
    main("E:\jackstudy\LetApiRun\data\Dface")