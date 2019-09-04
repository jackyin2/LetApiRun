#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : let_loader.py
@Author: JACK
@Date  : 2019/8/23
@Des   : 该方法主要从data目录中加载所有的目录下的json-api数据，统一存在到一个list中
"""
import os
import json
from let_init import GENARATE_RESULT, VALUEPOOLS


class Loader(object):

    def __init__(self):
        self.cases = []

    def __len__(self):
        return len(self.cases)

    def __getitem__(self, index):
        return self.cases[index]

    def load_cases_from_file(self, file_path):
        """
        从指定文件中加载case
        :param file_path: 
        :return: 
        """
        self._add_cases(file_path)

    def load_cases_from_dir(self, path):
        """
        从指定目录中加载测试
        :param path: 
        :return: 
        """
        # 从目录中加载测试用例
        files = self._discover_file_api(path)
        for file in files:
            self._add_cases(file)

    def _add_cases(self, path):
        """
        加载所有的json对象到cases列表中
        :param path: 
        :return: 
        """
        with open(path, "r", encoding="utf-8") as f:
            try:
                # f_dict = json.load(f).decode(encoding='gbk').encode(encoding='utf-8')
                f_dict = json.load(f)
            except Exception as e:
                print("读取的json文件存在错误{}，文件为：{}".format(e, path))
            else:
                self.cases.append(f_dict)

    def _discover_file_api(self, path):

        """
        查找所有的需要执行测试case文件
        :param path: 
        :return: 
        """
        files = []
        all_files = os.walk(path)
        for root, dirs, filenames in all_files:
            if filenames == []:
                continue
            else:
                for name in filenames:
                    # 区分测试用例文件和初始化参数文件
                    if name.startswith("test_") and \
                            (name.endswith(".json") or name.endswith(".yaml")):
                        files.append(os.path.join(root, name))
                    # if name.startswith("global_") and name.endswith(".py"):
                    #     pass
        return files
















