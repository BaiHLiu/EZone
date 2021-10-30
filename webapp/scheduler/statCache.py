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
    time_now = datetime.datetime.now()
    for dayDelta in range(0, 7):
        day = (time_now + datetime.timedelta(days=-dayDelta)).strftime("%Y-%m-%d")
        data = stat.getDailySum(day)
        rdsCache.rds.set(f'statistics:historyDays:{day}', json.dumps(data))


##########################################################
# 定时任务配置
def scheduleInit():
    rdsSetHistoryDaysData()
    rdsSetRTData()
# redis缓存实时状态
scheduler.add_job(rdsSetRTData, 'interval', seconds=60)
scheduler.add_job(rdsSetHistoryDaysData, 'interval', seconds=60)

##########################################################


if __name__ == "__main__":
    # rdsSetRTData()
    rdsSetHistoryDaysData()
