# -*- coding: utf-8 -*-
import logging

import arrow
from flask import Flask, request, jsonify
from flask_limiter import Limiter, HEADERS
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

from config import Production
from my_logger import debug_logging, online_logging, access_logging


app = Flask(__name__)
app.config.from_object(Production())

db = SQLAlchemy(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

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

from .views import home, token, user, gd_vehicle, hz_hbc

app.register_blueprint(home.blueprint, url_prefix='/')
app.register_blueprint(token.blueprint, url_prefix='/token')
app.register_blueprint(user.blueprint, url_prefix='/user')
app.register_blueprint(gd_vehicle.blueprint, url_prefix='/gdvehicle')
app.register_blueprint(hz_hbc.blueprint, url_prefix='/hzhbc')

@app.after_request
def after_request(response):
    """访问信息写入日志"""
    access_logger.info('%s - - [%s] "%s %s HTTP/1.1" %s %s'
                       % (request.remote_addr,
                          arrow.now().format('DD/MMM/YYYY:HH:mm:ss ZZ'),
                          request.method, request.path, response.status_code,
                          response.content_length))
    response.headers['Server'] = app.config['SERVER']
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message': 'Not Found'}), 404,
    {'Content-Type': 'application/json; charset=utf-8',
     'Server': app.config['SERVER']}

@app.errorhandler(405)
def method_not_allow(error):
    return jsonify({'message': 'Method Not Allowed'}), 405,
    {'Content-Type': 'application/json; charset=utf-8',
     'Server': app.config['SERVER']}

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal Server Error'}), 500,
    {'Content-Type': 'application/json; charset=utf-8',
     'Server': app.config['SERVER']}

