# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth, HTTPDigestAuth
from flask_limiter import Limiter, HEADERS
from peewee import SqliteDatabase, MySQLDatabase

from config import Production


# create a flask application - this ``app`` object will be used to handle
app = Flask(__name__)
app.config.from_object(Production())
api = Api(app)

db = SqliteDatabase(app.config['DATABASE'], journal_mode='WAL')
mysql_db = MySQLDatabase(
    app.config['MYSQLDB']['db'],
    user=app.config['MYSQLDB']['user'],
    password=app.config['MYSQLDB']['password'],
    host=app.config['MYSQLDB']['host']
)

auth = HTTPBasicAuth()

logger = logging.getLogger('root')

limiter = Limiter(app, headers_enabled=True, global_limits=["10/minute"])
limiter.header_mapping = {
    HEADERS.LIMIT : "X-RateLimit-Limit",
    HEADERS.RESET : "X-RateLimit-Reset",
    HEADERS.REMAINING: "X-RateLimit-Remaining"
}
