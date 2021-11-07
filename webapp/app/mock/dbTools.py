#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/29 8:52 PM
# @Author  : Catop
# @File    : dbTools.py
# @Software: PyCharm

import json
import sys

sys.path.append("../../../")

from webapp.utils import mysqlDB


def workTable():
    """
    补充buildingName信息
    :return:
    """
    devList = mysqlDB.dbGet("SELECT * FROM dev_info", [])
    for dev in devList:
        devId = dev['id']
        buildingName = str(dev['name']).split('-')[0]

        mysqlDB.dbSet("UPDATE dev_info SET buildingName=%s WHERE id=%s LIMIT 1", [buildingName, devId])

    return


def initRoomInfo():
    """
    写入房间信息
    :return:
    """
    with open('roomList.json') as f:
        data = json.load(f)

        # for room in data['spaces']:
        #     # print(room)
        #     mysqlDB.dbSet("INSERT INTO room_info SET name=%s,capacity=%s", [room['name'], room['capacity']])

        for subLocation in data['subLocations']:
            for room in subLocation['spaces']:
                # print(room)
                mysqlDB.dbSet("INSERT INTO room_info SET name=%s,capacity=%s", [room['name'], room['capacity']])


def copyDateData(src, dst):
    """
    复制某天数据，并将dst覆盖
    :param src: 来源日期
    :param dst: 目的日期
    :return:
    """

    mysqlDB.dbSet("DELETE FROM upload_log WHERE upload_time LIKE %s", [dst + '%'])
    srcData = mysqlDB.dbGet("SELECT * FROM upload_log WHERE upload_time LIKE %s", [src + '%'])

    for log in srcData:
        mysqlDB.dbSet("INSERT INTO upload_log(dev_id,people_num,upload_time) VALUES (%s,%s,%s)",
                      [
                          log['dev_id'],
                          log['people_num'],
                          dst + ' ' + str(log['upload_time']).split(' ')[1]
                      ])


if __name__ == "__main__":
    # print(workTable())
    # print(initRoomInfo())
    copyDateData('2021-11-03', '2021-11-07')