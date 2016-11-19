#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from . import db
from datetime import datetime


'''
    在用户类中，定义id、openid、省、市、县、头像、注册日期
'''

class User(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf-8mb4'
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(32), nullable=True)
    province = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(20), nullable=True)
    headimgurl = db.Column(db.String(150), nullable=True)
    regtime = db.Column(db.Datetime, default=datetime.now, nullable=False)

    def __init__(self, openid, name=None, province=None, city=None,
            country=None, headimgurl=None, regtime=None):
        self.openid = openid
        self.name = name
        self.province = province
        self.city = city
        self.country = country
        self.headimgurl = headimgurl
        self.regtime = regtime

    def __repr__(self):
        return '<openid %r>' %self.openid

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
