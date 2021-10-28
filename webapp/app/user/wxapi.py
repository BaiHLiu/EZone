#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/27 11:47 PM
# @Author  : Catop
# @File    : wxapi.py
# @Software: PyCharm

"""
请求微信服务端API
"""

import json

import requests

from webapp.config import wxConfig


class WXError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo

def code2Session(js_code):
    """
    登陆code获取openid和session_key
    :param js_code: 登陆code
    :return: dict
    """
    params = {
        'appid': wxConfig.appid,
        'secret': wxConfig.secret,
        'js_code': js_code,
        'grant_type': 'authorization_code'
    }

    req = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params)
    try:
        resp = json.loads(req.text)
        loginRet = {
            'openid': resp['openid'],
            'session_key': resp['session_key']
        }
    except:
        raise WXError("code2Session失败")
    else:
        return loginRet


if __name__ == "__main__":
    print(code2Session("081EEc0w3R06lX2ZSY2w3CyN9b2EEc0M"))


