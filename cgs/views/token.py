# -*- coding: utf-8 -*-
from functools import wraps

import arrow
from flask import g, Blueprint, request, jsonify
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .. import app, limiter, logger, access_logger
from ..models import Users

blueprint = Blueprint('token', __name__)

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

def get_uid():
    try:
        g.uid = -1
        g.scope = ''
        if request.json:
            user = Users.query.filter_by(username=request.json.get('username', ''),
                                         banned=0).first()
            if user:
                if sha256_crypt.verify(request.json.get('password', ''),
                                       user.password):
                    g.uid = user.id
                    g.scope = user.scope
                    return str(g.uid)
        return request.remote_addr
    except Exception as e:
        logger.error(e)
        raise

@blueprint.route('', methods=['POST'])
@limiter.limit("5/hour", get_uid)
@verify_addr
def token_post():
    try:
        if request.json is None:
            return jsonify({'message': 'Problems parsing JSON'}), 400
        if not request.json.get('username', None):
            error = {'resource': 'Token', 'field': 'username',
                     'code': 'missing_field'}
            return jsonify({'message': 'Validation Failed', 'errors': error}), 422
        if not request.json.get('password', None):
            error = {'resource': 'Token', 'field': 'password',
                     'code': 'missing_field'}
            return jsonify({'message': 'Validation Failed', 'errors': error}), 422

        if g.uid == -1:
            return jsonify({'message': 'username or password error'}), 422
        s = Serializer(app.config['SECRET_KEY'], expires_in=app.config['EXPIRES'])
        token = s.dumps({'uid': g.uid, 'scope': g.scope.split(',')})
    except Exception as e:
        logger.error(e)
        raise
    return jsonify({'uid': g.uid,
                    'access_token': token,
                    'token_type': 'self',
                    'scope': g.scope,
                    'expires_in': app.config['EXPIRES']}), 201,
    {'Cache-Control': 'no-store', 'Pragma': 'no-cache'}


