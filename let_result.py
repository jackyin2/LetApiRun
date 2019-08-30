#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : result.py
@Author: JACK
@Date  : 2019/8/23
@Des   :
"""


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


def result_return(GENARATE_RESULT):
    success = fail = time = 0

    for reobj in GENARATE_RESULT:
        if reobj.result == 1:
            success += 1
            time += reobj.time
        if reobj.result == 0:
            fail += 1
    avg_time = time/success
    return {"success": success, "fail": fail, "avg_time": avg_time}


class Reportor():
    pass


















