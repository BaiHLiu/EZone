#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/23 8:30 PM
# @Author  : Catop
# @File    : views.py
# @Software: PyCharm
import random

from flask import Blueprint, request, jsonify

import webapp.libs.apiResp as apiResp

mockApp = Blueprint('mockApp', __name__)


@mockApp.route('/get_building_status')
def get_building_available():
    buildingName = request.args.get('buildingName')
    if not (buildingName and len(buildingName) > 0):
        return apiResp.error('传入楼宇名称为空', -1)

    ret = []
    max_seats_list = [80, 120, 160, 200]
    for i in range(201, 240):
        max_seats = max_seats_list[random.randint(0, 3)]
        occupy_rate = random.randint(10, 90) / 100
        room_status = {
            'room_name': buildingName + '-' + str(i),
            'available': random.randint(0, 1),
            'max_seats': max_seats,
            'current_occupy': int(max_seats * occupy_rate),
            'occupy_rate': occupy_rate
        }

        ret.append(room_status)

    return apiResp.success(ret)
