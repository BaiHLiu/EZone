#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/29 9:01 PM
# @Author  : Catop
# @File    : statCache.py
# @Software: PyCharm
import datetime
import json

from apscheduler.schedulers.background import BackgroundScheduler

from webapp.app.statistics import stat
from webapp.logging import logger
from webapp.utils import mysqlDB
from webapp.utils import rdsCache

scheduler = BackgroundScheduler()

MODULE_NAME = 'scheduler.statCache'


def rdsSetRTData():
    """
    Redis缓存所有设备实时数据
    :return:
    """

    devList = mysqlDB.dbGet("SELECT * FROM dev_info", [])
    succFlag = 0
    try:
        for dev in devList:
            devId = dev['id']
            devNewestData = mysqlDB.dbGet(
                "SELECT people_num,upload_time FROM upload_log WHERE dev_id=%s ORDER BY id DESC LIMIT 1", [devId])
            if len(devNewestData) >= 1:
                peopleNum = devNewestData[0]['people_num']
            else:
                # 暂无记录
                peopleNum = 0
            rdsCache.rds.set(f'iot:devRT:{devId}', peopleNum)
    except:
        logger.error(MODULE_NAME, '缓存实时状态失败')
    else:
        logger.success(MODULE_NAME, '缓存实时状态成功')

    return


def rdsSetHistoryDaysData():
    """
    缓存近7天所有设备总数数据
    :return:
    """
    try:
        time_now = datetime.datetime.now()
        for dayDelta in range(0, 7):
            day = (time_now + datetime.timedelta(days=-dayDelta)).strftime("%Y-%m-%d")
            data = stat.getDailySum(day)
            rdsCache.rds.set(f'statistics:historyDays:{day}', json.dumps(data))
    except:
        logger.error(MODULE_NAME, '缓存7天所有设备总数数据失败')
    else:
        logger.success(MODULE_NAME, '缓存7天所有设备总数数据成功')


def rdsSetEachBuildingOverallRTData():
    """
    缓存各教学楼实时人数和占用率
    :return:
    """

    try:
        buildingList = mysqlDB.dbGet("SELECT name FROM building_info WHERE 1=1", [])
        retList = []

        for build in buildingList:
            # 总人数
            buildPeopleSum = 0
            # 总座位数
            buildCapacitySum = 0

            buildName = build['name']
            devList = mysqlDB.dbGet("SELECT * FROM dev_info WHERE buildingName=%s", [buildName])

            for dev in devList:

                devId = dev['id']
                devName = dev['name']
                capacity = mysqlDB.dbGet("SELECT capacity FROM room_info WHERE name LIKE %s", [devName + '%'])

                if len(capacity) > 0:
                    capacity = capacity[0]['capacity']
                else:
                    capacity = 50

                buildCapacitySum += int(capacity)
                people = mysqlDB.dbGet(
                    "SELECT people_num from upload_log WHERE dev_id=%s ORDER BY upload_time DESC LIMIT 1", [devId])
                if len(people) > 0:
                    people = people[0]['people_num']
                else:
                    people = 0

                buildPeopleSum += int(people)

            buildInfo = {
                'buildName': buildName,
                'buildPeopleSum': buildPeopleSum,
                'buildOccupyRate': round(buildPeopleSum / buildCapacitySum, 2),
                'buildRoomNum': len(devList),
            }
            retList.append(buildInfo)

        rdsCache.rds.set(f'statistics:EachBuildingOverallRTData', json.dumps(retList))

    except:
        logger.error(MODULE_NAME, '缓存各教学楼实时人数和占用率失败')
    else:
        logger.success(MODULE_NAME, '缓存各教学楼实时人数和占用率成功')

    return retList


##########################################################
# 定时任务配置
def scheduleInit():
    rdsSetHistoryDaysData()
    rdsSetRTData()
    rdsSetEachBuildingOverallRTData()


# redis缓存实时状态
scheduler.add_job(rdsSetRTData, 'interval', seconds=60)
scheduler.add_job(rdsSetHistoryDaysData, 'interval', seconds=120)
scheduler.add_job(rdsSetEachBuildingOverallRTData, 'interval', seconds=120)

##########################################################


if __name__ == "__main__":
    rdsSetRTData()
    # rdsSetHistoryDaysData()
    # print(rdsSetEachBuildingOverallRTData())
