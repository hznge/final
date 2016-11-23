#!/usr/bin/env python3
# -*- coding: utf-8

from .. import redis


def set_user_state(openid, state):
    """Set User State"""
    redis.hset('wechat:user:' + openid, 'state', state)
    return None


def get_user_state(openid):
    """Get User State"""
    return redis.hget('wechat:user:' + openid, 'state')


def set_user_last_interact_time(openid, timestamp):
    """Save the last interact time"""
    redis.hset('wechat:user:' + openid, 'last_interact_time', timestamp)
    return None


def get_user_last_interact_time(openid):
    """Get the last interact time"""
    last_time = redis.hget('wechat:user:' + openid, 'last_interact_time')
    return last_time if last_time else 0
