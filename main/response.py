#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from main import app
from .models import set_user_info
from .utils import AESCipher, init_wechat_sdk
from .plugins.state import set_user_state, get_user_state, \
    set_user_last_interact_time, get_user_last_interact_time
from .plugins import simsimi, wechat_custom


def wechat_response(data):
    """微信消息处理回复"""
    global message, openid, wechat

    wechat = init_wechat_sdk()
    wechat.parse_data(data)
    message = wechat.get_message()
    openid = message.source
    # 用户信息写入数据库
    set_user_info(openid)

    try:
        get_resp_func = msg_type_resp[message.type]
        response = get_resp_func()
    except KeyError:
        # 默认回复微信消息
        response = 'success'

    # 保存最后一次交互的时间
    set_user_last_interact_time(openid, message.time)
    return response


# 储存微信消息类型所对应函数（方法）的字典
msg_type_resp = {}


def set_msg_type(msg_type):
    """
    储存微信消息类型所对应函数（方法）的装饰器
    """

    def decorator(func):
        msg_type_resp[msg_type] = func
        return func

    return decorator


@set_msg_type('text')
def text_resp():
    """文本类型回复"""
    # 默认回复微信消息
    response = 'success'
    # 替换全角空格为半角空格
    message.content = message.content.replace(u'　', ' ')
    # 清除行首空格
    message.content = message.content.lstrip()
    # 指令列表
    commands = {
        u'取消': cancel_command,
        u'^\?|^？': all_command,
        u'^游戏|^遊戲': html5_games,
        u'陪聊': enter_chat_state,
        u'^绑定|^綁定': auth_url,
        u'更新菜单': update_menu_setting
    }
    # 状态列表
    state_commands = {
        'chat': chat_robot,
    }
    # 匹配指令
    command_match = False
    for key_word in commands:
        if re.match(key_word, message.content):
            # 指令匹配后，设置默认状态
            set_user_state(openid, 'default')
            response = commands[key_word]()
            command_match = True
            break
    if not command_match:
        # 匹配状态
        state = get_user_state(openid)
        # 关键词、状态都不匹配，缺省回复
        if state == 'default' or not state:
            response = command_not_found()
        else:
            response = state_commands[state]()
    return response


@set_msg_type('click')
def click_resp():
    """菜单点击类型回复"""
    commands = {
        'chat_robot': enter_chat_state,

    }
    # 匹配指令后，重置状态
    set_user_state(openid, 'default')
    response = commands[message.key]()
    return response


@set_msg_type('subscribe')
def subscribe_resp():
    """订阅类型回复"""
    set_user_state(openid, 'default')
    response = subscribe()
    return response


def chat_robot():
    """聊天机器人"""
    timeout = int(message.time) - int(get_user_last_interact_time(openid))
    if timeout > 20 * 60:
        set_user_state(openid, 'default')
        content = app.config['CHAT_TIMEOUT_TEXT'] + app.config['HELP_TEXT']
        return wechat.response_text(content)
    else:
        simsimi.chat.delay(openid, message.content)
        return 'success'


def update_menu_setting():
    """更新自定义菜单"""
    try:
        wechat.create_menu(app.config['MENU_SETTING'])
    except Exception as e:
        return wechat.response_text(e)
    else:
        return wechat.response_text('Done!')


def enter_chat_state():
    """进入聊天模式"""
    set_user_state(openid, 'chat')
    return wechat.response_text(app.config['ENTER_CHAT_STATE_TEXT'])


def command_not_found():
    """非关键词回复"""
    # 客服接口回复信息
    content = app.config['COMMAND_NOT_FOUND_TEXT'] + app.config['HELP_TEXT']
    wechat_custom.send_text(openid, content)
    # 转发消息到微信多客服系统
    return wechat.group_transfer_message()


def all_command():
    """回复全部指令"""
    content = app.config['COMMAND_TEXT']
    return wechat.response_text(content)


def subscribe():
    """回复订阅事件"""
    content = app.config['WELCOME_TEXT'] + app.config['COMMAND_TEXT']
    return wechat.response_text(content)
