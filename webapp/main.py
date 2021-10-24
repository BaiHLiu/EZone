#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 11:46 AM
# @Author  : Catop
# @File    : main.py
# @Software: PyCharm
import os
import sys

p = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
if p not in sys.path:
    sys.path.append(p)


from flask import Flask

from app.iot.views import *
from app.mock.views import *
from app.user.views import *
from config import webAppConfig

# 创建app
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(iot, url_prefix='/iotApi')
app.register_blueprint(userAPI, url_prefix='/userAPI')
app.register_blueprint(mockApp, url_prefix='/mock')

if __name__ == '__main__':
    app.run(host=webAppConfig.host, port=webAppConfig.port)
