# -*- coding: utf-8 -*-
import os


class Config(object):
    # 密码 string
    SECRET_KEY = 'hellokitty'
    # 主机IP string
    HOST = '0.0.0.0'
    # 服务名称
    SERVER = 'SX-CgsServer'
    # 加密次数 int
    ROUNDS = 123456
    # token生存周期，默认1小时 int
    EXPIRES = 3600
    # 数据库连接 string
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../cgs.db'
    # 数据库连接 dict
    SQLALCHEMY_BINDS = {
        'cgs': 'mysql://root:root@127.0.0.1/cgs'
    }
    # 用户权限范围 dict
    SCOPE_USER = {}
    # 白名单启用 bool
    WHITE_LIST_OPEN = True
    # 白名单列表 set
    WHITE_LIST = set(['127.0.0.1'])


class Develop(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
