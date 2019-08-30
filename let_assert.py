#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_assert.py
@Author: JACK
@Date  : 2019/8/28
@Des   : 主要是用于扩展检查几个校验方式，code， str， json， headers
"""
import json
from let_utils import reg_str


def assertEqCode(r, vali):
    if vali.get("status_code") is None or r.status_code == vali["status_code"]:
        return True
    return False


def assertEqHeaders(r, vali):
    if vali.get("headers") is None:
        return False
    else:
        n = 0
        for k, v in vali["headers"].items():
            if vali["headers"][k] == r.headers[k]:
                n += 1
        if n == len(vali["headers"]):
            return True
    return False


def assertEqStr(r, vali):
    if vali.get("assertEqStr") is None:
        return False
    else:
        num = 0
        l = vali["assertEqStr"]
        for s in l:
            # 正则search
            if reg_str(s, r.text):
                num += 1
        if num == len(l):
            return True
    return False


def assertEqJson(r, vali):
    if vali.get("assertEqJson") is None:
        return False
    try:
        jt = json.loads(r.text)
    except:
        print("assertEqJson出错了", end="")
    vl = vali["assertEqJson"]
    m = 0
    for k, v in vl.items():
        if jt.get(k) is None:
            print("response找不到validator中的的json字段---", end="")
            return False
        if vl[k] == jt[k]:
            m += 1
    if m == len(vl):
        return True
    return False

