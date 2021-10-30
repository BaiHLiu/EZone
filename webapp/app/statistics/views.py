#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/28 9:30 AM
# @Author  : Catop
# @File    : view.py
# @Software: PyCharm
# 数据接口

from flask import Blueprint, request

import json
import webapp.libs as libs
from webapp.app.statistics import stat
from webapp.utils import mysqlDB
from webapp.utils import rdsCache

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

    sqlRet = mysqlDB.dbGet("SELECT name FROM building_info", [])
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
        # mysql查询已弃用，改为redis
        # retData = stat.getDailySum(date)
        retData = json.loads(rdsCache.rds.get(f'statistics:historyDays:{date}'))
    except:
        return libs.apiResp.error(-1)
    else:
        return libs.apiResp.success(body=retData)


@statisticsAPI.route('/getBuildingStatus', methods=['GET'])
def getBuildingStatus():
    """
    获取指定教学楼所有教室实时状态
    :return:
    """
    urlParams = getReqData(request)
    buildingName = urlParams['buildingName']
    retList = {}

    buildingDevList = mysqlDB.dbGet("SELECT id FROM dev_info WHERE buildingName=%s", [buildingName])

    for dev in buildingDevList:
        devId = dev['id']
        devName = stat.getDevInfo(devId)[0]['name']
        peopleNum = rdsCache.rds.get(f'iot:devRT:{devId}')
        if peopleNum:
            retList[devName] = peopleNum
        else:
            retList[devName] = 0

    return libs.apiResp.success(body=retList)


@statisticsAPI.route('/getRoomStatus', methods = ['GET'])
def getRoomStatus():
    """
    获取指定教室状态（当前人数、满载人数、当日历史）
    :return:
    """

    urlParams = getReqData(request)
    # 教室名称：J1-101
    roomName = urlParams['roomName']

