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


if __name__ == "__main__":
    # print(workTable())
    print(initRoomInfo())
