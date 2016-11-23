#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from redis import Redis
from .plugins.queue import make_celery

app = Flask(__name__, instance_relative_config=True)
# 加载配置
app.config.from_object('config')
app.config.from_pyfile('config.py')

# 队列
celery = make_celery(app)

# 记录日志
handlers = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handlers.setFormatter(logging.Formatter(
    '%(asctime)s  %(levelname)s: %(message)s '
    '[in %(pathname)s: %(lineno)d]'
))
handlers.setLevel(logging.WARNING)
app.logger.addHandler(handlers)

# init the 3 part lib
redis = Redis()

# Router
from .routes import *
# 定时任务
from .plugins import *
