# -*- coding: utf-8 -*-
import os


class Config(object):
    DEBUG = True
    SECRET_KEY = 'hellokitty'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    # 主机IP
    HOST = '0.0.0.0'
    # 端口
    PORT = '8099'
    # 数据库
    DATABASE = 'cgs.db'
    # mysqldb
    MYSQLDB = {'db': 'cgs', 'host': 'localhost',
               'user': 'root', 'password': 'root'}
    # 加密次数, int
    ROUNDS = 123456
    # token生存周期，默认1小时 int
    EXPIRES = 3600

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../cgs.db'
    SQLALCHEMY_BINDS = {
        'cgs': 'mysql://root:root@localhost/cgs'
    }
    # 用户权限范围 dict
    SCOPE_USER = {}


class Develop(Config):
    pass


class Production(Config):
    DEBUG = False
