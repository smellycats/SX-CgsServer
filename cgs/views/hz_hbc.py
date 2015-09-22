# -*- coding: utf-8 -*-
import urlparse
import urllib
from functools import wraps

import arrow
from flask import g, Blueprint, request, jsonify

from .. import app, limiter, logger, access_logger
from ..models import HbcAll, HZVehicle
from ..helper_url import *

blueprint = Blueprint('hzhbc', __name__)

def verify_addr(f):
    """IP地址白名单"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not app.config['WHITE_LIST_OPEN'] or request.remote_addr == '127.0.0.1' or request.remote_addr in app.config['WHITE_LIST']:
            pass
        else:
            return {'status': '403.6',
                    'error': u'禁止访问:客户端的 IP 地址被拒绝'}, 403
        return f(*args, **kwargs)
    return decorated_function

def verify_token(f):
    """token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if not request.headers.get('Access-Token'):
                return {'status': '401.6', 'message': 'missing token header'}, 401
            token_result = verify_auth_token(request.headers['Access-Token'],
                                             app.config['SECRET_KEY'])
            if not token_result:
                return {'status': '401.7', 'message': 'invalid token'}, 401
            elif token_result == 'expired':
                return {'status': '401.8', 'message': 'token expired'}, 401
            g.uid = token_result['uid']
            g.scope = set(token_result['scope'])
        except Exception as e:
            logger.error(e)
            raise
        return f(*args, **kwargs)
    return decorated_function

def verify_scope(f):
    """token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            scope = '_'.join(request.blueprint, request.method.lower())
        except Exception as e:
            logger.error(e)
        if 'all' in g.scope or scope in g.scope:
            pass
        else:
            return {'status': 405, 'error': 'Method Not Allowed'}, 405
        return f(*args, **kwargs)
    return decorated_function

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
@verify_addr
@limiter.limit("60/minute")
@verify_token
def index():
    items = []
    try:
        hbc = HbcAll.query.join(HZVehicle, HZVehicle.xh == HbcAll.nxh).filter(HZVehicle.hphm == HbcAll.hphm).all()
        for i in hbc:
            items.append({'hphm': i.hphm, 'hpzl': i.hpzl})
    except Exception as e:
        logger.error(e)
        raise
    return jsonify({'total_count': len(items), 'items': items}), 200
