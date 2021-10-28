#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 11:38 AM
# @Author  : Catop
# @File    : views.py
# @Software: PyCharm
import json
import datetime

from flask import Blueprint, request
import webapp.libs as libs
from webapp.utils import mysqlDB

iotAPI = Blueprint('iotAPI', __name__)

@iotAPI.route('/upload', methods=['POST'])
def show():
    data = libs.request.request_parse(request)
    retDict = json.loads(data['body'])
    time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    for imgName in retDict.keys():
        try:
            dev_id = int(imgName.split('/')[-1].split('.')[0])
            people_num = int(retDict[imgName])
            mysqlDB.dbSet("INSERT INTO upload_log(dev_id,people_num,upload_time) VALUES (%s,%s,%s)",[dev_id,people_num,time])
        except:
            continue

    return libs.apiResp.success()
