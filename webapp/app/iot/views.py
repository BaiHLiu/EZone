#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 11:38 AM
# @Author  : Catop
# @File    : views.py
# @Software: PyCharm
import json

from flask import Blueprint, request
import webapp.libs as libs
from webapp.utils import mysqlDB

iotAPI = Blueprint('iotAPI', __name__)

@iotAPI.route('/upload', methods=['POST'])
def show():
    data = libs.request.request_parse(request)
    body = json.loads(data['body'])

    print(body)

    return 'iot.hello'
