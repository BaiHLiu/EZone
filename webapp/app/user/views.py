#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 11:39 AM
# @Author  : Catop
# @File    : views.py
# @Software: PyCharm
from flask import Blueprint, request

import webapp.libs as libs
from webapp.utils import mysqlDB

userAPI = Blueprint('userAPI', __name__)


def getReqData(request):
    data = libs.request.request_parse(request)
    return data


@userAPI.route('/register', methods=['POST'])
def register():
    data = getReqData(request)
    try:
        params = [data['name'], data['type'], data['department'], data['openid'], data['session_key']]
        mysqlDB.dbSet("INSERT INTO userinfo(name,type,department,openid,session_key) VALUES (%s,%s,%s,%s,%s)", params)

    except:
        ret = libs.apiResp.error(-1, '注册失败')
    else:
        ret = libs.apiResp.success(prompt='注册成功')

    return ret


@userAPI.route('/login', methods=['POST'])
def login():
    data = getReqData(request)

    params = [data['openid']]

    userInfo = mysqlDB.dbGet("SELECT * FROM userinfo WHERE openid=%s", params)
    try:
        userInfo = userInfo[0]

        params = [data['session_key'], data['openid']]
        mysqlDB.dbSet("UPDATE userinfo SET session_key=%s WHERE openid=%s LIMIT 1", params)
    except:
        ret = libs.apiResp.error(-1, '登陆失败')
    else:
        ret = libs.apiResp.success('登陆成功', userInfo)

    return ret


@userAPI.route('/check_status', methods=['GET'])
def checkStatus():
    '''检查登陆状态'''
    data = getReqData(request)
    openid = data['openid']
    session_key = data['session_key']
    # 验证当前skey与最后skey时候相同

    try:
        userInfo = mysqlDB.dbGet("SELECT * FROM userinfo WHERE openid=%s", [openid])[0]
        validKey = userInfo['session_key']
        if (validKey == session_key):
            ret = libs.apiResp.success(msg='1',body=userInfo, prompt='已登陆')
        else:
            ret = libs.apiResp.success(msg='0',prompt='未登陆')
    except:
        ret = libs.apiResp.error(-1,prompt='未注册')

    return ret
