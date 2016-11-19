#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from flask import request, render_template, jsonify, Markup, abort, \
    send_from_directory
from . import app, redis
from .utils import check_signature, get_jsapi_signature_data
from .models import is_user_exists
import ast

@app.route("/", methods=['GET', 'POST'])
@check_signature
def handle_wechat_request():
    '''
    处理回复微信请求
    '''
    if request.method == 'POST':
        return wechat_response(request.data)
    else:
        # 微信的接入认证
        return request.args.get('echostr', '')

@app.route('/auth-order-room/<openid>', methods=['GET', 'POST'])
def auth_order_room:
    if request.method == 'POST':

    elif is_user_exists():

    else:
        abort(404)
