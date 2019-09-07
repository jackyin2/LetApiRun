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


class ApiCase(object):

    def __init__(self):
        self._fname = None
        self._fobj = None

    def __str__(self):
        return "<%s testApi=%s>" % \
               (strclass(self.__class__), self._fobj)

    def __repr__(self):
        return "<%s testApi=%s>" % \
               (strclass(self.__class__), self._fobj)

    @property
    def filename(self):
        return self._fname

    @filename.setter
    def filename(self, f):
        self._fname = f

    @property
    def fileobj(self):
        return self._fobj

    @fileobj.setter
    def fileobj(self, f):
        self._fobj = f


















    def __str__(self):
        return ""

    def __repr__(self):
        return ""
