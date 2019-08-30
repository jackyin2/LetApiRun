#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_response.py
@Author: JACK
@Date  : 2019/8/23
@Des   :
"""


class Response(object):
    def __init__(self):
        self._code = None
        self._body = None
        self._header = None

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, context):
        self._body = context

