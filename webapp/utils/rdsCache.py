#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/28 12:17 AM
# @Author  : Catop
# @File    : rdsCache.py
# @Software: PyCharm

import redis
import uuid

from webapp.config import redisConfig as rdsConf

rds = redis.StrictRedis(host=rdsConf.host, port=rdsConf.port, db=rdsConf.db, decode_responses=rdsConf.decode_responses)


def sigToken(openid):
    """
    签发token
    :param openid:
    :return:
    """
    token = uuid.uuid4()
    # 双向键：user:token:{openid}->token
    #       user:openid:{token}->openid
    rds.set(f'user:token:{str(openid)}', str(token))
    rds.set(f'user:openid:{str(token)}', str(openid))

    return token


def veriToken(openid):
    """
    读取用户token
    :param openid:
    :return:
    """

    keyName = f'user:token:{openid}'

    return rds.get(keyName)



if __name__ == "__main__":
    print(sigToken('test'))
    print(veriToken('test'))
