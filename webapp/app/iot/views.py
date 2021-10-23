#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 11:38 AM
# @Author  : Catop
# @File    : views.py
# @Software: PyCharm
from flask import Blueprint

iot = Blueprint('iot', __name__)


@iot.route('/test')
def show():
    return 'iot.hello'
