#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#__author__ = 'Hznge'
from main import app

if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run()
