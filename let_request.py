#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_request.py
@Author: JACK
@Date  : 2019/8/23
@Des   :
"""
import requests


class Http(object):

    def __init__(self):
        self.http = requests

    def get(self, url, params=None, **kwargs):
        return self.http.get(url, params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.http.post(url, data, json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.http.put(url, data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.http.patch(url, data, **kwargs)

    def delete(self, url, **kwargs):
        return self.http.delete(url, **kwargs)


class Https(object):
    pass
