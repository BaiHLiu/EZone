#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/29 8:52 PM
# @Author  : Catop
# @File    : dbTools.py
# @Software: PyCharm

from webapp.utils import mysqlDB


def workTable():
    """
    补充buildingName信息
    :return:
    """
    devList = mysqlDB.dbGet("SELECT * FROM dev_info",[])
    for dev in devList:
        devId = dev['id']
        buildingName = str(dev['name']).split('-')[0]

        mysqlDB.dbSet("UPDATE dev_info SET buildingName=%s WHERE id=%s LIMIT 1", [buildingName, devId])


    return



if __name__ == "__main__":
    print(workTable())