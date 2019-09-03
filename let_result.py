#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : result.py
@Author: JACK
@Date  : 2019/8/23
@Des   :
"""


from jinja2 import Template
from let_init import GENARATE_RESULT

class ApiResult(object):
    def __init__(self):
        self._api_name = None
        self._result = False
        self._error = ""
        self._message = None
        self._time = 0

    def append(self, GENARATE_RESULT):
        GENARATE_RESULT.append(self)

    @property
    def api_name(self):
        return self._api_name

    @api_name.setter
    def api_name(self, api):
        self._api_name = api

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, val):
        self._result = val

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, val):
        self._time = val

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, val):
        self._error = val

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, val):
        self._message = val


class Reportor(object):
    """
    report生成器
    """
    def __init__(self,  report_name, type=None, genarate_result=GENARATE_RESULT):
        self.template = "./templeate/report_template.html"
        self.genarate_result = genarate_result
        self.report_name = report_name
        self.type = type
        self.r = None

    def _read_template(self):
        print("---read_report---")
        with open(self.template, 'r', encoding='UTF-8') as f:
            t = f.read()
            tp = Template(t)
            self.r = tp.render(success=self._count_success(), all=self._count_all(), fail=self._count_failure(), fail_messages=self._get_failure_message(), avgtime=self._avg_time(),
                               maxtime=self._max_time(), mintime=self._min_time())
        return self.r

    def _new_report(self):
        print("---report-success---")
        with open("./report/"+self.report_name, 'w') as f:
            f.write(self.r)

    def _is_report(self):
        pass

    def _report(self):
        if self.report_name.endswith(self.type):
            self._read_template()
            self._new_report()
        else:
            print("当前生成的报告非指定格式{}".format(self.type))

    def _count_all(self):
        return len(self.genarate_result)

    def _count_success(self):
        return len([s for s in self.genarate_result if s.result == True])

    def _count_failure(self):
        return len([f for f in self.genarate_result if f.result == False])

    def _get_failure_message(self):
        return [f for f in self.genarate_result if f.result == False]

    def _avg_time(self):
        return sum([t.time for t in self.genarate_result])/self._count_all()

    def _max_time(self):
        return max([t.time for t in self.genarate_result])

    def _min_time(self):
        return min([t.time for t in self.genarate_result])


class HtmlReportor(Reportor):

    def __init__(self, report_name, type):
        super(HtmlReportor,self).__init__(report_name, type)

    def report(self):
        print("*********report*******")
        self._report()


class TextReportor(Reportor):
    def __init__(self, report_name):
        super(TextReportor,self).__init__(report_name)

    def report(self):
        self._report()






















