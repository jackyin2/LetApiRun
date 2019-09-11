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
        self._file_name = None
        self._case_name = None
        self._request = None
        self._validate = None
        self._collect = None
        self._response = ""
        self._result = None
        self._message = ""
        self._time = 0

    @property
    def filename(self):
        return self._file_name

    @filename.setter
    def filename(self, f):
        self._file_name = f

    @property
    def casename(self):
        return self._case_name

    @casename.setter
    def casename(self, c):
        self._case_name = c

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, r):
        self._request = r

    @property
    def validate(self):
        return self._validate

    @validate.setter
    def validate(self, v):
        self._validate = v

    @property
    def collect(self):
        return self._collect

    @collect.setter
    def collect(self, c):
        self._collect = c

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, r):
        self._response = r

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, r):
        self._result = r

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, m):
        self._message = m

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, t):
        self._time = t


class ApiCase(BaseCase):
    def __init__(self):
        super(ApiCase, self).__init__()
        self._type = 'API'

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t):
        self._type = t


class File(object):
    """
    记录所有的文件转换的json的case
    """
    def __init__(self):
        self._f_name = None
        self._f_obj = None    # json.load(f)获取
        self._f_path = None
        self._f_mes = None
        self._f_result = None

    def __str__(self):
        return "<%s testApi=%s>" % \
               (strclass(self.__class__), self._f_obj)

    def __repr__(self):
        return "<%s testApi=%s>" % \
               (strclass(self.__class__), self._f_obj)

    @property
    def filename(self):
        return self._f_name

    @filename.setter
    def filename(self, f):
        self._f_name = f

    @property
    def fileobj(self):
        return self._f_obj

    @fileobj.setter
    def fileobj(self, f):
        self._f_obj = f

    @property
    def filemes(self):
        return self._f_mes

    @filemes.setter
    def filemes(self, f):
        self._f_mes = f

    @property
    def fileresult(self):
        return self._f_result

    @fileresult.setter
    def fileresult(self, f):
        self._f_result = f

    @property
    def filepath(self):
        return self._f_path

    @filepath.setter
    def filepath(self, f):
        self._f_path = f





