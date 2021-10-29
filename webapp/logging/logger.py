#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/29 9:39 PM
# @Author  : Catop
# @File    : logger.py
# @Software: PyCharm

import time


def success(module, msg, status=0):
    print(f"[+] {module}: {msg} - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")


def error(module, msg, status=-1):
    print(f"[!] {module}: {msg} - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
