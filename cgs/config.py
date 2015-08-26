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
    #mysqldb
    MYSQLDB = {'db': 'cgs', 'host': 'localhost',
               'user': 'root', 'password': 'root'}
    # 加密次数
    ROUNDS = 123456
    # token生存周期，默认1小时
    EXPIRES = 3600

class Develop(Config):
    pass


class Production(Config):
    DEBUG = False
