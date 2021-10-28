#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/28 9:30 AM
# @Author  : Catop
# @File    : view.py
# @Software: PyCharm
# 数据接口

from flask import Blueprint, request

import webapp.libs as libs
from webapp.utils import mysqlDB
from webapp.utils import rdsCache
from webapp.app.statistics import stat

statisticsAPI = Blueprint('statisticsAPI', __name__)

# alias
def getReqData(request):
    data = libs.request.request_parse(request)
    return data

@statisticsAPI.route('/getBuildings', methods=['GET'])
def getBuildings():
    """
    获取所有楼宇名称
    :return:
    """

    sqlRet = mysqlDB.dbGet("SELECT name FROM building_info",[])
    buildingList = []
    for build in sqlRet:
        buildingList.append(build['name'])

    return libs.apiResp.success(body=buildingList)


@statisticsAPI.route('/getDailySumData', methods=['GET'])
def getDailySumData():
    """
    获取指定天所有设备合计记录
    :return:
    """

    urlParams = getReqData(request)
    # 日期，格式为'2021-10-26'
    date = urlParams['date']
    try:
        retData = stat.getDailySum(date)
    except:
        return libs.apiResp.error(-1)
    else:
        return libs.apiResp.success(body=retData)





