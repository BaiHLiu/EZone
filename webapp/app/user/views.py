#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 11:39 AM
# @Author  : Catop
# @File    : views.py
# @Software: PyCharm
from flask import Blueprint

user=Blueprint('user',__name__)

@user.route('/')
def show():
    return 'user.hello'