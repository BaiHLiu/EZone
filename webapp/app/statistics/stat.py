#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/28 9:51 AM
# @Author  : Catop
# @File    : stat.py
# @Software: PyCharm
# 用于统计数据

from webapp.utils import mysqlDB
from webapp.utils import rdsCache


def getDevInfo(devId):
    """
    获取设备信息
    :param devId:
    :return:
    """
    sqlRet = mysqlDB.dbGet("SELECT * FROM dev_info WHERE id = %s", [devId])
    return sqlRet


def getDailySum(date):
    """
    获取指定日期当天所有设备总数变化
    :param date: 日期格式为'2021-10-26'
    :return:
    """
    sqlRet = mysqlDB.dbGet("SELECT dev_id,people_num,upload_time FROM upload_log WHERE upload_time LIKE %s", [date+'%'])
    # 提取每个时间点总数
    timelyData = {}
    for upinfo in sqlRet:
        devId = upinfo['dev_id']
        peopleNum = upinfo['people_num']
        upTime = str(upinfo['upload_time'])

        if upTime in timelyData.keys():
            timelyData[upTime] += peopleNum
        else:
            timelyData[upTime] = peopleNum


    return timelyData

if __name__ == '__main__':
    print(getDevInfo(7))
    print(getDailySum('2021-10-26'))
