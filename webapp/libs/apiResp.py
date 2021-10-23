#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 8:50 PM
# @Author  : Catop
# @File    : error.py
# @Software: PyCharm

from flask import jsonify


def error(msg, err_code, body=None):
    ret = {
        'msg': msg,
        'err_code': err_code,
        'body': body
    }

    return jsonify(ret)


def success(body=None):
    ret = {
        'msg': 'ok',
        'err_code': 0,
        'body': body
    }

    return jsonify(ret)
