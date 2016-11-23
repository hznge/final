#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from celery.schedules import crontab

DEBUG = False

# 应用网址
HOST_URL = "http://"

# 微信公众号配置
APP_ID = "wxf3688f21233542e9"
APP_SECRET = "946720f9077c9b4b9fef42aee61b1b21"
TOKEN = "hello"
EncodingAESKey = ""

# 数据库
SQLALCHEMY_DATABASE_URI = "mysql://user:password@host/dbname?charset=utf-8mb4"

# celery 配置
CELERY_BROKEN_URL = 'redis://ip:port'
CELERY_RESULT_BCAKEND = 'redis://ip:port'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERUBEAT_SCHEDULE = {
    'every-15-min-at-8-to-22': {
        'task': 'access_token.update',
        'schedules': crontab(minute=0, hour='*/1')
    }
}

# SimSimi key
SIMSIMI_KEY = ''
