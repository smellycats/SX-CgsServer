# -*- coding: utf-8 -*-
import urlparse
import urllib
from functools import wraps

import arrow
from flask import g, Blueprint, request, jsonify

from .. import app, cache, limiter, logger, access_logger
from ..models import GDVehicle, Csys
from ..helper_url import *

blueprint = Blueprint('gdvehicle', __name__)

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

@cache.memoize(3600) # 缓存1小时
def get_vehicle(hphm='', hpys=None):
    vehicle = GDVehicle.query.filter_by(hphm=hphm)
    if hpys:
        hpzl = []
        if hpys in set([u'blue', u'蓝', u'2']):
            hpzl = ('02', '08')
        elif hpys in set([u'yellow', u'黄', u'3']):
            hpzl = ('01', '07', '13', '14', '15', '16', '17')
        elif hpys in set([u'white', u'白', u'4']):
            hpzl = ('20', '21', '22', '24', '32')
        elif hpys in set([u'black', u'黑', u'5']):
            hpzl = ('03', '04', '05', '06', '09', '10', '11', '12')
        else:
            hpzl = ()
        vehicle = vehicle.filter(GDVehicle.hpzl.in_(hpzl))
    return vehicle.all()

@blueprint.route('')
@verify_addr
@verify_token
def index():
    result = {'gdvehicle_url': '%sgdvehicle/:hphm{/:hpys}' % request.url_root}
    return jsonify(result), 200, {'Cache-Control': 'public, max-age=60, s-maxage=60'}


@blueprint.route('/<string:hphm>')
@blueprint.route('/<string:hphm>/<string:hpys>')
@verify_addr
@limiter.limit("5000/hour")
@verify_token
def gdvehicle_get(hphm, hpys=None):
    try:
        vehicle = get_vehicle(hphm, hpys)
        items = []
        for i in vehicle:
            items.append({'id': i.id, 'hpzl': i.hpzl, 'clxh': i.clxh,
                          'clpp1': i.clpp1, 'clpp2': i.clpp2, 'zzcmc': i.zzcmc,
                          'clsbdh': i.clsbdh, 'fdjh': i.fdjh, 'cllx': i.cllx,
                          'csys': i.csys, 'syr': i.syr, 'fzrq': i.fzrq,
                          'hphm': i.hphm})
    except Exception as e:
        logger.error(e)
    return jsonify({'total_count': len(items), 'items': items}), 200,
    {'Cache-Control': 'public, max-age=60, s-maxage=60'}
