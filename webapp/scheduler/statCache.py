#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/29 9:01 PM
# @Author  : Catop
# @File    : statCache.py
# @Software: PyCharm

from apscheduler.schedulers.background import BackgroundScheduler

from webapp.utils import mysqlDB
from webapp.utils import rdsCache
from webapp.logging import logger

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


##########################################################
# 定时任务配置

# redis缓存实时状态
scheduler.add_job(rdsSetRTData, 'interval', seconds=60)

##########################################################




if __name__ == "__main__":
    rdsSetRTData()