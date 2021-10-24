#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 8:50 PM
# @Author  : Catop
# @File    : error.py
# @Software: PyCharm

from flask import jsonify


def error(err_code, prompt='操作失败', msg='error', body=None):
    ret = {
        'msg': msg,
        'err_code': err_code,
        'body': body,
        'prompt': prompt
    }

    return jsonify(ret)


def success(prompt='操作成功', body=None, msg='ok'):
    ret = {
        'msg': msg,
        'err_code': 0,
        'body': body,
        'prompt': prompt
    }

    return jsonify(ret)
