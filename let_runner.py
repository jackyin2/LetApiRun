#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_runner.py
@Author: JACK
@Date  : 2019/8/23
@Des   : 执行脚本
"""

import requests
import time
import os
import json
from let_init import GENARATE_RESULT, VALUEPOOLS
from let_loader import Loader
from let_result import ApiResult
from let_utils import *
from let_assert import assertEqCode, assertEqHeaders, assertEqStr, assertEqJson
from let_parserconf import ParserConf
from functools import wraps

from addict import Dict


count = 0


def start_end_decorator(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        end = time.time()
        runtime = start - end
    return wrapper

# def start_end_decorator(fun):
#     @wraps(fun)
#     def decorated_function(*args, **kwargs):
#         return fun(*args, **kwargs)
#     return decorated_function


class Runner(object):
    def __init__(self, path=None, file=None, report=None):
        self.test_dir = path
        self.test_api = file
        self.report_path = report
        self.loader = Loader()
        self.init_variable()

    def loader_file(self):
        # 执行单个api
        self.loader.load_cases_from_file(self.test_api)
        return self.loader

    def loader_dir(self):
        # 执行项目目录下的api
        self.loader.load_cases_from_dir(self.test_dir)
        return self.loader

    def init_variable(self):
        # 初始化加载全局配置
        for root, dirs, filenames in os.walk(self.test_dir):
            if filenames == []:
                continue
            else:
                for name in filenames:
                    # 区分测试用例文件和初始化参数文件
                    if name.startswith("Init") and name.endswith(".ini"):
                        conf_path = root+"\\"+name
                        p = ParserConf(conf_path)
                        p.conf_2_valuepool(VALUEPOOLS)
                    break
            break

    def run(self):
        # 判断是单文件执行还是批量执行
        if self.test_dir is None and self.test_api is not None:
            self.loader_file()
        elif self.test_dir is not None and self.test_api is None:
            self.loader_dir()
        elif self.test_dir is not None and self.test_api is not None:
            print("不允许path和file同时存在")
        elif self.test_dir is not None and self.test_api is not None:
            print("path和file不允许同时为空")

        # check loader是否有内容
        if len(self.loader) > 0:
            for test_case in self.loader:

                cases = test_case["test"]
                # 区分开是存在多用例，还是单用例
                if type(cases) is list:
                    for case in cases:
                        global count
                        count += 1
                        print("*****当前执行第 {} 个 case：{}********".format(count,case["name"]), end=":")
                        if case["setupcase"]:
                            v = self._setup(case)
                        else:
                            print("---start---no setup---")
                        self._runapi(case, v)
                        if case["teardowncase"]:
                            self._teardown(case, v)
                        else:
                            print("---end---no teardown---")
                else:
                    print("*****当前执行的case：{}********".format(cases["name"]))
                    if cases["setupcase"]:
                        v = self._setup(cases)
                    else:
                        print("---start---no setup---")
                    self._runapi(cases, v)
                    if cases["teardowncase"]:
                        self._teardown(cases, v)
                    else:
                        print("---end---no teardown---")
        else:
            print("当前没有需要执行的用例，请检查是否有错误")

    def _setup(self, case):
        """
        setup 需要注意，在填写相关的部分时，必须按照正常kv，方法kv，方法参数kv的顺序填写，不允许乱序，
        否则会出现参数化失败的情况
        :param case: 
        :return: 
        """
        print("---start---setup---", )
        vals = case["setupcase"]
        _vals = {}
        # 首先_vals先加载方法中不存在$的方法和正常的值
        for key, val in vals.items():
            # 判断是否是一个待执行的方法，
            method = is_method(str(val))
            if method:
                if is_params(method):
                    continue
                # 判断当前的方法是否还需要继续参数化，如果需要参数化，则等待后面执行
                _vals[key] = eval(method)
            elif not method:
                _vals[key] = val
            else:
                pass
                
        for k, v in vals.items():
            method = is_method(str(v))
            if method and is_params(method):
                method = parameters(method, _vals, VALUEPOOLS)
                _vals[k] = eval(method)
        return _vals

    def _runapi(self, case, v_setup):
        print("----api---", end="")
        # 执行api方法, 此处注意返回的parameter是一个字符串，后续需要进行相关处理
        url = parameters(case["requestor"]["url"], v_setup, VALUEPOOLS)
        method = case["requestor"]["method"].upper()
        headers = json.loads(parameters(case["requestor"]["headers"], v_setup, VALUEPOOLS))
        data = json.loads(parameters(case["requestor"]["data"], v_setup, VALUEPOOLS))

        # 声明一个结果收集
        apiresult = ApiResult()
        start = time.time()
        if method == "GET":
            re = requests.get(url, headers=headers)
        elif method == "POST":
            if headers["content-type"] == "application/json":
                try:
                    re = requests.post(url=url, headers=headers, json=data, timeout=2)
                    # print(re.headers)
                    # print(re.cookies.get_dict())
                    # print(re.text)
                    # print(re.status_code)
                    # print(re.url)
                    # print(re.encoding)
                    # print(re.request)
                except Exception as e:
                    print("当前url：{}， 响应超时".format(url))
                    re = None
                    apiresult.error = e
                finally:
                    pass
            else:
                re = requests.post(url=url, headers=headers, data=data)
            # json转换
        elif method == "PUT":
            pass
        elif method == "DELETE":
            pass
        elif method == "PATCH":
            pass
        end = time.time()

        # 校验器
        if self._valitor(re, case["validator"]):
            apiresult.result = True
        else:
            apiresult.error = "validator---校验字段出错+"

        runtime = end - start

        apiresult.api_name = case["name"]
        if re is None:
            apiresult.message = "error"
        else:
            apiresult.message = re.text
        apiresult.time = runtime
        apiresult.append(GENARATE_RESULT)
        # del apiresult

        # 收集器
        if not self._collector(re, case["collector"]):
            apiresult.error += "collector---收集出错"

    def _teardown(self, case, setup):
        """
        清理当前case中的预条件setupcase中的内容，
        :param case: 
        :param setup: 
        :return: 
        """
        if len(setup) > 0:
            clear_value(setup)
            print("---end---teardown---")
        else:
            print("---end---no-teardown")
        return

    def _valitor(self, re, vali):
        """
        校验器， 用于校验case中validator中的条件是否正确
        :param re: 
        :param vali: 
        :return: 
        """
        if re is None:
            return False
        # 校验成功判断
        count = 0
        if assertEqCode(re, vali):
            count += 1
        if assertEqStr(re, vali):
            count += 1
        if assertEqHeaders(re, vali):
            count += 1
        if assertEqJson(re, vali):
            count += 1
        if count == len(vali):
            print("success")
            return True
        if count < len(vali):
            print("fail")
        return False

    def _collector(self, re, coll):
        """
        收集器，回收一个公共参数，比如获取token后期使用，直接通过
        :param re: 
        :param coll: 
        :return: 
        """
        if re is None:
            return False
        try:
            response = json.loads(re.text)
        except Exception as e:
            print("解析{}json格式错误,错误信息{}".format(re, e))
            return False
        response = Dict(response)
        for k, v in coll.items():
            # 此处判断如果是json，则用链式取值，如果是方法，则用正则来进行匹配获取
            if k == "json":
                for k1,v1 in v.items():
                    # 通过eval直接执行获取对应的json值
                    v1 = eval(v1)
                    VALUEPOOLS[k1] = v1
                    # VALUEPOOLS.update(k1=v1)
            elif k == "methods":
                for k2, v2 in v.items():
                    if "${__" in str(v2):
                        VALUEPOOLS[k2] = eval(is_method(v2))
            else:
                pass
        return True

    def report(self):
        count_all = len(GENARATE_RESULT)
        time_ = count_fail = count_success = 0
        for obj in GENARATE_RESULT:
            if obj.result is True:
                count_success += 1
                time_ += obj.time
            elif obj.result is False:
                count_fail += 1
                print("用例；{}，响应信息{}，错误信息：{}， ".format(obj.api_name, obj.message, obj.error ))
        obj_time_list = [obj.time for obj in GENARATE_RESULT]
        avg_time = sum(obj_time_list)/count_all
        max_time = max(obj_time_list)
        min_time = min(obj_time_list)
        print("总计执行cases：{}个， 成功：{}个， 失败：{}个, 平均响应时间：{}, 其中最大响应时间{}， 最小响应时间{}".format(count_all, count_success, count_fail, avg_time, max_time, min_time))

