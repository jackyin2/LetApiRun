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
from let_exceptions import *
from functools import wraps
from requests_toolbelt import MultipartEncoder

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
    def __init__(self, path=None, file=None, init_conf=None):
        self.test_dir = path
        self.test_api = file
        self.loader = Loader()
        self.init_conf = init_conf

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

        # 1 判断是否需要初始化配置
        if self.init_conf:
            self.init_variable()
        # 2 判断是单文件执行还是批量执行
        if self.test_dir is not None and self.test_api is None:
            self.loader_dir()
        elif self.test_dir is not None and self.test_api is not None:
            self.loader_file()
        elif self.test_dir is None and self.test_api is None:
            print("请检查你是否未填写path和file")
            exit(0)
        # 3 check loader是否有内容
        if len(self.loader) > 0:
            for _case in self.loader:
                global count
                count += 1
                # 判断加载的file对象是否为空，如果为空，咋不执行，否则进行请求操作
                if _case.request is None:
                    print("*****当前执行第 {} 个 case：{}, message: {}********".format(count, _case.request, _case.message))
                    GENARATE_RESULT.append(_case)
                    continue
                print("*****当前执行第 {} 个 case：{}********".format(count, _case.casename))
                if _case.request["setupcase"]:
                    v = self._setup(_case)
                else:
                    print("---start---no setup---")
                self._runapi(_case, v)
                if _case.request["teardowncase"]:
                    self._teardown(_case, v)
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
        print("1: start---setup", )
        vals = case.request["setupcase"]
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
                # 如果不要参数化，判断下是不是路径式字段是则转换
                _vals[key] = replace_path(val)
            else:
                pass
        # 此处加载方法中带有参数$
        for k, v in vals.items():
            method = is_method(str(v))
            if method and is_params(method):
                method = parameters(method, _vals, VALUEPOOLS)
                _vals[k] = eval(method)
        return _vals

    def _runapi(self, case, v_setup):
        """
        执行api，并判断校验，同时处理收集需要的值
        :param file: 
        :param case: 
        :param v_setup: 
        :return: 
        """
        print("2: api > ", end="")
        # apiresult = ApiResult()
        # 执行api方法, 此处注意返回的parameter是一个字符串，后续需要进行相关处理
        try:
            url = parameters(case.request["requestor"]["url"], v_setup, VALUEPOOLS)
            method = parameters(case.request["requestor"]["method"], v_setup, VALUEPOOLS).upper()
            headers = json.loads(parameters(case.request["requestor"]["headers"], v_setup, VALUEPOOLS))
            data = json.loads(parameters(case.request["requestor"]["data"], v_setup, VALUEPOOLS))
            params = None
        except NotFoundParams as e:
            print("error: {}".format(e))
            case.message = "[params error {}]\n".format(e)
        #  此处判断是否存在文件需要处理
        if case.request.get("requestor").get("files"):
            filedicts = json.loads(parameters(case.request["requestor"]["files"], v_setup, VALUEPOOLS))
            _files = {}
            for filekey, filevalue in filedicts.items():
                _files[filekey] = post_files(replace_path(filevalue))


        start = time.time()

        try:
            if method == "GET":
                re = requests.get(url=url, params=data, headers=headers)
            elif method == "POST":
                if headers.get("content-type") and headers["content-type"] == "application/json":
                    re = requests.post(url=url, headers=headers, json=data, timeout=2)
                else:
                    re = requests.post(url=url, headers=headers, data=data, files=_files, timeout=2)
                # json转换
            elif method == "PUT":
                pass
            elif method == "DELETE":
                pass
            elif method == "PATCH":
                re = requests.patch(url=url, headers=headers, data=data, files=_files, timeout=2)
        except Exception as e:
            print("当前url：{}， 响应超时, {}".format(url, e))
            re = None
            case.result = False
            case.message += "[request error: {}]\n".format(e)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        end = time.time()
        # print(re.text)

        # 校验器
        if re is not None:
            try:
                validate_params = self._valitor(re, case.request["validator"])
            except NotEqualError as e:
                case.result = False
                case.message = "[validator error: {}]\n".format(e)
                case.validate = "N"
                print("error:{}".format(e))
            except JsonError as e:
                case.result = False
                case.message = "[validator error: {}]\n".format(e)
                case.validate = "N"
                print("error:{}".format(e))
            else:
                if validate_params:
                    case.result = True
                    case.validate = "Y"

        runtime = end - start
        if re is not None:
            case.response = re.text
        else:
            case.response = "error"
        case.time = runtime
        # case.append(GENARATE_RESULT)
        GENARATE_RESULT.append(case)
        # del apiresult

        # 收集器
        if re is not None:
            try:
                self._collector(re, case.request["collector"])
            except JsonError as e:
                case.message += "[collector error: {}]\n".format(e)
                print("error: {}".format(e))
                case.collect = "N"
            except EvalError as e:
                case.message += "[collector error: {}]\n".format(e)
                print("error: {}".format(e))
                case.collect = "N"
            else:
                case.collect = "Y"

    def _teardown(self, case, setup):
        """
        清理当前case中的预条件setupcase中的内容，
        :param case: 
        :param setup: 
        :return: 
        """
        if len(setup) > 0:
            clear_value(setup)
            print("3: end---teardown")
            print()
        else:
            print("3: end---no-teardown")
            print()
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
        try:
            response = json.loads(re.text)
        except Exception as e:
            print("解析{}json格式错误,错误信息{}".format(re, e))
            raise NotJsonError(re.text)
            # return False

        response = Dict(response)
        for k, v in coll.items():
            # 此处判断如果是json，则用链式取值，如果是方法，则用正则来进行匹配获取
            if k == "json":
                for k1,v1 in v.items():
                    # 通过eval直接执行获取对应的json值
                    try:
                        v1 = eval(v1)
                    except Exception:
                        raise EvalError(v1, "Json_collect")
                    VALUEPOOLS[k1] = v1
                    # VALUEPOOLS.update(k1=v1)
            elif k == "methods":
                for k2, v2 in v.items():
                    if "${__" in str(v2):
                        try:
                            VALUEPOOLS[k2] = eval(is_method(v2))
                        except Exception:
                            raise EvalError(is_method(v2), "Method_collect")
            else:
                pass

    def report_to_ctr(self):
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

