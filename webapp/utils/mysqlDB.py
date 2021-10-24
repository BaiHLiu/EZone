#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 9:01 AM
# @Author  : Catop
# @File    : dbconn.py
# @Software: PyCharm

import pymysql

from webapp.config import mysqlConfig


def dbGet(sql, params):
    '''
    数据库查询操作
    :param sql: sql语句
    :return: 查询的所有结果字典
    '''
    conn = pymysql.connect(host=mysqlConfig.host, port=mysqlConfig.port, user=mysqlConfig.username,
                           passwd=mysqlConfig.password, db=mysqlConfig.db, charset='utf8')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, params)
    data = cursor.fetchall()

    return data


def dbSet(sql, params):
    '''
    数据库增删改操作
    :param sql: sql语句
    :return: 受影响行数或主键id
    '''
    conn = pymysql.connect(host=mysqlConfig.host, port=mysqlConfig.port, user=mysqlConfig.username,
                           passwd=mysqlConfig.password, db=mysqlConfig.db, charset='utf8')

    cursor = conn.cursor()
    effectRow = cursor.execute(sql, params)
    if sql.split(' ')[0] == 'INSERT':
        insertId = conn.insert_id()
        conn.commit()
        return insertId
    else:
        conn.commit()
        return effectRow






def test():
    sql = "INSERT INTO userinfo(name,type,department,openid,session_key) VALUES(%s,%s,%s,%s,%s)"
    params = ['catop', 'staff', 'jsj', '86693852', 'kJtdi6RF+Dv67QkbLlPGjw==']
    dbSet(sql, params)


if __name__ == "__main__":
    test()
