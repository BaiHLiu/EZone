#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 9:51 AM
# @Author  : Catop
# @File    : request.py
# @Software: PyCharm
import json


def request_parse(req_data):
    '''
    解析请求数据并以json返回
    :param req_data:
    :return:请求数据json
    '''
    if req_data.method == 'POST':
        data = req_data.form
    elif req_data.method == 'GET':
        data = req_data.args

    return dict(data)
