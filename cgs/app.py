# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth, HTTPDigestAuth
from flask_limiter import Limiter, HEADERS
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

from config import Production
from cgs import debug_logging, online_logging, access_logging


# create a flask application - this ``app`` object will be used to handle
app = Flask(__name__)
app.config.from_object(Production())
api = Api(app)

db = SQLAlchemy(app)

auth = HTTPBasicAuth()

debug_logging(u'logs/error.log')
access_logging(u'logs/access.log')

logger = logging.getLogger('root')
access_logger = logging.getLogger('access')

limiter = Limiter(app, headers_enabled=True, global_limits=["10/minute"])
limiter.header_mapping = {
    HEADERS.LIMIT: "X-RateLimit-Limit",
    HEADERS.RESET: "X-RateLimit-Reset",
    HEADERS.REMAINING: "X-RateLimit-Remaining"
}

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
