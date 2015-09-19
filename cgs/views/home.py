# -*- coding: utf-8 -*-
import arrow
from flask import Blueprint, request, jsonify

from .. import app, limiter, logger, access_logger

blueprint = Blueprint('home', __name__)

@app.after_request
def after_request(response):
    """访问信息写入日志"""
    access_logger.info('%s - - [%s] "%s %s HTTP/1.1" %s %s'
                       % (request.remote_addr,
                          arrow.now().format('DD/MMM/YYYY:HH:mm:ss ZZ'),
                          request.method, request.path, response.status_code,
                          response.content_length))
    response.headers['Server'] = app.config['SERVER']
    return response

@blueprint.route('')
@blueprint.route('/')
def index():
    result = {
        'user_url': '%suser{/:user_id}' % (request.url_root),
        'scope_url': '%suser/scope' % (request.url_root),
        'token_url': '%stoken' % (request.url_root),
        'gdvehicle_url': '%sgdvehicle/:hphm{/:hpys}' % (request.url_root),
        'hzhbc_url': '%shzhbc/:hphm/:hpzl' % (request.url_root)
    }
    return jsonify(result), 200, {'Cache-Control': 'public, max-age=60, s-maxage=60'}



