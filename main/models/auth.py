#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from . import db

class Auth(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf-8mb4'
    }

    openid = db.Column(db.String(32), primary_key=True, unique=True,
                        nullable=False)
    custormid = db.Column(db.String(20), nullable=True)
    custormpasswd = db.Column(db.String(100), nullable=True)
    custormphone = db.Column(db.String(11), nullable=True)

    def __init__(self, openid, custormid=None, custormpasswd=None,
                custormphone=None):
        self.openid = openid
        self.custormid = custormid
        self.custormpasswd = custormpasswd
        self.custormphone = custormphone

    def __repr__(self):
        return '<openid %r>' %self.openid

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
