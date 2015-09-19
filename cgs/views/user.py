# -*- coding: utf-8 -*-
import arrow
from flask import Blueprint, request, jsonify
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .. import app, limiter, logger, access_logger
from ..models import Users, Scope

blueprint = Blueprint('user', __name__)


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
@limiter.limit("5000/hour")
def index():
    try:
        users = Users.query.all()
        items = []
        for user in users:
            items.append({'id': user.id,
                          'username': user.username,
                          'scope': user.scope,
                          'date_created': str(user.date_created),
                          'date_modified': str(user.date_modified),
                          'banned': user.banned})
    except Exception as e:
        logger.error(e)
    return jsonify({'total_count': len(items), 'items': items}), 200

@blueprint.route('/<int:user_id>')
@limiter.limit("5000/hour")
def user_get(user_id):
    user = Users.query.filter_by(id=user_id, banned=0).first()
    if user:
        return jsonify({'id': user.id,
                        'username': user.username,
                        'scope': user.scope,
                        'date_created': str(user.date_created),
                        'date_modified': str(user.date_modified),
                        'banned': user.banned}), 200
    else:
        return jsonify(), 404

@blueprint.route('', methods=['POST'])
@blueprint.route('/', methods=['POST'])
@limiter.limit("60/minute")
def user_post():
    if not request.json.get('username', None):
        error = {'resource': 'Token', 'field': 'username',
                 'code': 'missing_field'}
        return {'message': 'Validation Failed', 'errors': error}, 422
    if not request.json.get('password', None):
        error = {'resource': 'Token', 'field': 'username',
                 'code': 'missing_field'}
        return {'message': 'Validation Failed', 'errors': error}, 422

    user = Users.query.filter_by(username=request.json['username'],
                                 banned=0).first()
    if not user:
        password_hash = sha256_crypt.encrypt(request.json['password'],
                                             rounds=app.config['ROUNDS'])
        # 所有权限范围
        all_scope = set()
        for i in Scope.query.all():
            all_scope.add(i.name)
        # 授予的权限范围
        request_scope = set(request.json.get('scope', u'null').split(','))
        # 求交集后的权限 u_scope = ','.join(all_scope & request_scope)
        u = Users(username=request.json['username'], password=password_hash,
                  scope=','.join(all_scope & request_scope), banned=0)
        db.session.add(u)
        db.session.commit()
        return {
            'id': u.id,
            'username': u.username,
            'scope': u.scope,
            'date_created': str(u.date_created),
            'date_modified': str(u.date_modified),
            'banned': u.banned
        }, 201
    else:
        return {'error': 'username is already esist'}, 422

@blueprint.route('/<int:user_id>', methods=['PUT'])
@limiter.limit("60/minute")
def user_put(user_id):
    try:
        # 所有权限范围
        all_scope = set()
        for i in Scope.query.all():
            all_scope.add(i.name)
        # 授予的权限范围
        request_scope = set(request.json.get('scope', u'null').split(','))
        # 求交集后的权限
        u_scope = ','.join(all_scope & request_scope)

        db.session.query(Users).filter_by(id=user_id).update(
            {'scope': u_scope, 'date_modified': arrow.now().datetime})
        db.session.commit()

        user = Users.query.filter_by(id=user_id).first()
        app.config['SCOPE_USER'][user.id] = set(user.scope.split(','))

        return jsonify(), 204
    except Exception as e:
        print (e)

@blueprint.route('/<int:user_id>', methods=['DELETE'])
@limiter.limit("10/minute")
def user_delete(user_id):
    try:
        db.session.query(Users).filter_by(id=user_id).update(
            {'banned': 1, 'date_modified': arrow.now().datetime})
        db.session.commit()

        return jsonify(), 204
    except Exception as e:
        print (e)

@blueprint.route('/scope')
def scope_get():
    scope = Scope.query.all()
    items = []
    for i in scope:
        items.append({'id': i.id, 'name': i.name})
    return jsonify({'total_count': len(items), 'items': items}), 200

@blueprint.route('/token')
def post(self):
    # verify_scope('token_post')
    if not request.json.get('username', None):
        error = {'resource': 'Token', 'field': 'username',
                 'code': 'missing_field'}
        return {'message': 'Validation Failed', 'errors': error}, 422
    if not request.json.get('password', None):
        error = {'resource': 'Token', 'field': 'username',
                 'code': 'missing_field'}
        return {'message': 'Validation Failed', 'errors': error}, 422
    if g.uid == -1:
        return {'message': 'username or password error'}, 422
    s = Serializer(app.config['SECRET_KEY'],
                   expires_in=app.config['EXPIRES'])
    token = s.dumps({'uid': g.uid, 'scope': g.scope.split(',')})
    return {'uid': g.uid,
            'access_token': token,
            'token_type': 'self',
            'scope': g.scope,
            'expires_in': app.config['EXPIRES']}, 201,
    {'Cache-Control': 'no-store', 'Pragma': 'no-cache'}


