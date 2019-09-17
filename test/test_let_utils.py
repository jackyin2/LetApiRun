#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : test_let_utils.py
@Author: JACK
@Date  : 2019/8/26
@Des   :
"""
import re, json

a = {
    "a1":1,
    "b1":{
        "bb":"${abc}"
    }
}

a1 = {
    "a1":1,
    "b1":{
        "bb":"${abc}"
    }
}
c = "a"
astr = "/device-mgr${ab}/#/login/${abc}/${c}"

# print(obj = re.sub("\$\{"+str(i)+"\}")

a = astr.split("$")
for i in a:
    if "{" not in i:
        a.remove(i)
print(a)
l = list()
for c in a:
    val = re.match("^\{(.*)\}", c).group(1)
    l.append(val)
print(l)


pattern = '\$\{(.+?)\}'
l2 = re.findall(pattern, json.dumps(a1))
print(l2, type(l2))


# astr2 = re.sub("\$\{[a-zA-Z0-9]*\}", c, astr)
astr2 = re.sub("\$\{ab\}", c, astr)
print(astr2)







'''
print(a)
print(eval("a.b1.bb"))
a = re.match("^\$\{(.*)\}", a.b1.bb)
print(a.group(1))
c = "$abc"
abc = 1

a = re.match("^\$(.*)", c)
print(type(a.group(1)))

import json
print(json.dumps(a1))
print(re.findall("\$\{", json.dumps(a1)))


'''


a = [1, 2, 3]
for i in a:
    if i == 1 :
        pass
    elif i == 2:
        pass
    elif i == 3:
        pass




