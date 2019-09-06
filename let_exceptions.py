#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_exceptions.py
@Author: JACK
@Date  : 2019/9/6
@Des   : 自定义一些异常类
"""
import sys


class MyExcepiton(Exception):
    def __str__(self):
        return ("异常：{}".format(self.__class__.__name__))


class JsonError(MyExcepiton):
    """
    所有Json相关的错误父类
    """
    def __init__(self, j=None):
        self.j = j
    pass


class ParseJsonError(JsonError):
    def __init__(self, j=None):
        self.j = j

    def __str__(self):
        return ("exception：{}, message：parse json {} error ".format(self.__class__.__name__, self.j))


class NotJsonError(JsonError):
    def __str__(self):
        return ("exception：{}, message：{} is not json ".format(self.__class__.__name__, self.j))


class NotEqualError(MyExcepiton):
    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def __str__(self):
        return ("exception：{}, message： {} != {}".format(self.__class__.__name__, self.a, self.b))
