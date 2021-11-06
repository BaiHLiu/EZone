#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/28 9:51 AM
# @Author  : Catop
# @File    : stat.py
# @Software: PyCharm
# 用于统计数据

from webapp.utils import mysqlDB


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
    sqlRet = mysqlDB.dbGet("SELECT dev_id,people_num,upload_time FROM upload_log WHERE upload_time LIKE %s",
                           [date + '%'])
    # 提取每个时间点总数
    timelyData = {}
    for upinfo in sqlRet:
        devId = upinfo['dev_id']
        peopleNum = upinfo['people_num']
        upTime = str(upinfo['upload_time'])
        # 分钟统一化处理：10的[0,5]倍
        upMin = int(int(upTime.split(':')[1])/10)
        upMin = upMin*10
        upMin = str(upMin).zfill(2)

        # 秒数统一化处理为0
        upTime = upTime.split(':')[0]+':'+upMin+':00'


        if upTime in timelyData.keys():
            timelyData[upTime] += peopleNum
        else:
            timelyData[upTime] = peopleNum

    return timelyData


def getDayData(roomName, date):
    """
    获取指定教室指定一天的人数数据
    :param roomName: eg:'J1-101'
    :param date: eg:'2021-10-29'
    :return: dict
    """
    retDict = {}
    devId = mysqlDB.dbGet("SELECT id FROM dev_info WHERE name=%s", [roomName])[0]['id']

    uploadList = mysqlDB.dbGet("SELECT people_num,upload_time FROM upload_log WHERE dev_id=%s AND upload_time LIKE %s",
                               [devId, date + '%'])
    for up in uploadList:
        retDict[str(up['upload_time'])] = up['people_num']

    return retDict


def getRangeDaysData(roomName, dayBegin, dayEnd):
    """
    获取指定教室N天范围内的每日总数
    :param roomName:
    :param dayBegin:
    :param dayEnd:
    :return:
    """


if __name__ == '__main__':
    # print(getDevInfo(7))
    # print(getDailySum('2021-10-26'))
    print(getDayData('S1-413', '2021-10-27'))
