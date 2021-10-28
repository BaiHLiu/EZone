#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 11:39 AM
# @Author  : Catop
# @File    : views.py
# @Software: PyCharm
from flask import Blueprint, request

import webapp.libs as libs
from webapp.app.user import wxapi
from webapp.utils import mysqlDB
from webapp.utils import rdsCache

userAPI = Blueprint('userAPI', __name__)

# alias
def getReqData(request):
    data = libs.request.request_parse(request)
    return data


@userAPI.route('/register', methods=['POST'])
def register():
    data = getReqData(request)
    try:
        code = data['code']
        try:
            sessionInfo = wxapi.code2Session(code)
        except Exception as err:
            return libs.apiResp.error(-1, str(err))

        # 禁止重复注册
        userInfo = mysqlDB.dbGet("SELECT * FROM userinfo WHERE openid=%s", sessionInfo['openid'])
        if len(userInfo) > 0:
            return libs.apiResp.error(-2, '已注册过，请直接登陆')

        params = [data['name'], data['type'], data['department'], sessionInfo['openid'], sessionInfo['session_key']]
        mysqlDB.dbSet("INSERT INTO userinfo(name,type,department,openid,session_key) VALUES (%s,%s,%s,%s,%s)", params)

    except:
        ret = libs.apiResp.error(-1, '注册失败')
    else:
        ret = libs.apiResp.success(prompt='注册成功')

    return ret


@userAPI.route('/login', methods=['POST'])
def login():
    data = getReqData(request)
    # 微信js_code
    code = data['code']
    # 获取openid和session_key
    try:
        sessionInfo = wxapi.code2Session(code)
    except Exception as err:
        return libs.apiResp.error(-1, str(err))

    # 签发token
    openid = sessionInfo['openid']
    session_key = sessionInfo['session_key']

    # 判断用户注册
    params = [openid]
    userInfo = mysqlDB.dbGet("SELECT * FROM userinfo WHERE openid=%s", params)
    if len(userInfo) == 0:
        ret = libs.apiResp.error(-2, '用户未注册')
    else:
        try:
            # 返回登陆信息
            userInfo = userInfo[0]
            token = rdsCache.sigToken(openid)
            retData = {
                'name': userInfo['name'],
                'type': userInfo['type'],
                'department': userInfo['department'],
                'openid': userInfo['openid'],
                'token': token
            }
            params = [session_key, openid]
            mysqlDB.dbSet("UPDATE userinfo SET session_key=%s WHERE openid=%s LIMIT 1", params)
        except Exception as e:
            ret = libs.apiResp.error(-1, '登陆失败')
            print(e)
        else:
            ret = libs.apiResp.success('登陆成功', retData)

    return ret


@userAPI.route('/check_status', methods=['GET'])
def checkStatus():
    '''检查登陆状态'''
    data = getReqData(request)
    openid = data['openid']
    token = data['token']

    validToken = rdsCache.veriToken(openid)
    if validToken == token:
        params = [openid]
        # 查询并返回用户信息
        userInfo = mysqlDB.dbGet("SELECT * FROM userinfo WHERE openid=%s", params)
        if len(userInfo) == 0:
            ret = libs.apiResp.error(-2, '用户未注册')
        else:
            # 返回登陆信息
            userInfo = userInfo[0]
            retData = {
                'name': userInfo['name'],
                'type': userInfo['type'],
                'department': userInfo['department'],
                'openid': userInfo['openid'],
            }

        ret = libs.apiResp.success(body=retData, msg='1')
    else:
        ret = libs.apiResp.success(msg='0')

    return ret
