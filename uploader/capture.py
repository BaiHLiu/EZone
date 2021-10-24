#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 3:09 PM
# @Author  : Catop
# @File    : capture.py
# @Software: PyCharm

import os
import zipfile
from datetime import datetime
from ftplib import FTP

import requests
import cv2

from webapp.config import uploaderConfig
from webapp.utils import mysqlDB

IMAGE_PATH = './images/'


def getCamList():
    '''从数据库查询摄像机列表'''
    dbList = mysqlDB.dbGet("SELECT id,ip FROM dev_info", [])
    return dbList


def getImgFromList():
    '''
    从列表下载图片
    :param folder_path: 存储位置
    :param poolFlag: 线程标记
    :return: None
    '''
    camList = getCamList()
    for camInfo in camList:
        id = camInfo['id']
        ip = camInfo['ip']

        # if(id % threadsNum == poolFlag):
        try:
            url = f'rtsp://{uploaderConfig.cam_username}:{uploaderConfig.cam_password}@{ip}:554/Streaming/Channels/101'
            cap = cv2.VideoCapture(url)
            ret, frame = cap.read()
            cap.release()
            cv2.destroyAllWindows()

            file_name = f'{str(id)}.jpg'
            cv2.imwrite(IMAGE_PATH + file_name, frame, [cv2.IMWRITE_JPEG_QUALITY, 80])  # 存储为图像
            print(f'[+]Successfully:{id} in {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        except:
            print(f'[!]Failed:{id} in {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')


def zipDir(dirpath, outFullName):
    '''
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName:  压缩文件保存路径+XXXX.zip
    :return: 无
    '''
    zip = zipfile.ZipFile(outFullName, 'w', zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标和路径，只对目标文件夹下边的文件及文件夹进行压缩（包括父文件夹本身）
        this_path = os.path.abspath('.')
        fpath = path.replace(this_path, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()
    print("[+]压缩文件成功")


def uploadFTP(fileName):
    try:
        f = FTP()
        f.connect(uploaderConfig.ftp_host, uploaderConfig.ftp_port, 30)
        f.login(uploaderConfig.ftp_username, uploaderConfig.ftp_password)
        f.cwd('/')
        file = open(fileName, 'rb')
        f.storbinary('STOR %s' % os.path.basename(fileName), file)
        file.close()
        f.quit()
    except:
        print("[!]文件上传FTP失败")
    else:
        print("[+]文件上传FTP成功")

def callDetector():
    '''调用yolox http api'''
    requests.get(uploaderConfig.detector_api)
    print("[+]调用识别接口成功")


def work():
    try:
        getImgFromList()
        zipDir('./images/', './tmpFiles/out.zip')
        uploadFTP('./tmpFiles/out.zip')
    except:
        print("[!]任务失败")
    else:
        print("[+]成功完成所有任务")


if __name__ == "__main__":
    # work()
    uploadFTP('./tmpFiles/out.zip')
