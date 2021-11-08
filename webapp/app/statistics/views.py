#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/28 9:30 AM
# @Author  : Catop
# @File    : view.py
# @Software: PyCharm
# 数据接口

import json
import random

from flask import Blueprint, request

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

    # 0=实时，1=其他时间
    timeType = 0

    if 'date' in urlParams.keys() and 'period' in urlParams.keys():
        day = urlParams['date']
        period = urlParams['period']
        timeType = 1

    retList = {}

    buildingDevList = mysqlDB.dbGet("SELECT id FROM dev_info WHERE buildingName=%s", [buildingName])

    for dev in buildingDevList:
        devId = dev['id']
        devName = stat.getDevInfo(devId)[0]['name']
        capacity = mysqlDB.dbGet("SELECT capacity FROM room_info WHERE name LIKE %s", [devName + '%'])

        if len(capacity) >= 1:
            capacity = capacity[0]['capacity']
        else:
            # 无信息教室默认100人容量
            capacity = 100

        if timeType == 0:
            # 实时
            peopleNum = rdsCache.rds.get(f'iot:devRT:{devId}')
            if peopleNum:
                occupt_rate = int(peopleNum) / int(capacity)
                if(occupt_rate * 1.2 < 1):
                    occupt_rate *= 1.2
                #TODO:使用真实数据
                retList[devName] = {'peopleNum': int(peopleNum), 'capacity': int(capacity), 'available': random.randint(0,1),
                                    'occupy_rate': round(occupt_rate,2)}
            else:
                retList[devName] = {'peopleNum': 0, 'capacity': 100, 'available': 1, 'occupy_rate': round(0, 2)}
        else:
            # 其他时间
            retList[devName] = {'peopleNum': 0, 'capacity': int(capacity), 'available': random.randint(0, 1),
                                'occupy_rate': round(1, 2)}

    return libs.apiResp.success(body=retList)


@statisticsAPI.route('/getRoomStatus', methods=['GET'])
def getRoomStatus():
    """
    获取指定教室状态（当前人数、满载人数、指定日信息）
    :return:
    """

    urlParams = getReqData(request)
    # 教室名称：J1-101
    roomName = urlParams['roomName']
    date = urlParams['date']

    devId = mysqlDB.dbGet("SELECT id FROM dev_info WHERE name=%s", [roomName])[0]['id']
    currentPeople = int(rdsCache.rds.get(f'iot:devRT:{devId}'))
    capacity = mysqlDB.dbGet("SELECT capacity FROM room_info WHERE name LIKE %s", [roomName + '%'])[0]['capacity']
    dayData = stat.getDayData(roomName, date)

    retBody = {
        'currentPeople': currentPeople,
        'capacity': capacity,
        'dayData': dayData
    }

    return libs.apiResp.success(body=retBody)


@statisticsAPI.route('/getEachBuildingOverallRTData', methods=['GET'])
def getEachBuildingOverallRTData():
    """
    各教学楼实时人数和占用率
    :return:
    """
    data = json.loads(rdsCache.rds.get('statistics:EachBuildingOverallRTData'))

    return libs.apiResp.success(body=data)

