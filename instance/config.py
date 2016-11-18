#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from celery.schedules import crontab

DEBUG = False

#应用网址
HOST_URL = "http://"

#微信公众号配置
APP_ID = ""
APP_SECRET = ""
TOKEN = ""
EncodingAESKey = ""

#数据库
SQLALCHEMY_DATABASE_URI = "mysql://user:password@host/dbname?charset=utf-8mb4"

#celery 配置
CELERY_BROKEN_URL = 'redis://ip:port'
CELERY_RESULT_BCAKEND = 'redis://ip:port'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERUBEAT_SCHEDULE = {
    'every-15-min-at-8-to-22': {
        'task': 'access_token.update',
        'schedules': crontab(minute=0, hour='*/1')
    }
}
