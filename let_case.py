#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_runner.py
@Author: JACK
@Date  : 2019/8/23
@Des   : case
"""
from let_utils import strclass


class BaseCase(object):
    def __init__(self):
        self._test_name = None
        self._test_setup = None
        self._test_teardown = None
        self._test_url = None

    def __repr__(self):
        return "<%s testMethod=%s>" % \
               (strclass(self.__class__), self._test_name)


class ApiCase(BaseCase):

    def __init__(self):
        super(ApiCase, self).__init__()
        self.a = None















    def __str__(self):
        return ""

    def __repr__(self):
        return ""
