# -*- coding: utf-8 -*-
import arrow
from flask import Blueprint, request, jsonify
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .. import app, limiter, logger
from ..models import Users, Scope

blueprint = Blueprint('user', __name__)


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
        return jsonify({'id': u.id,
                        'username': u.username,
                        'scope': u.scope,
                        'date_created': str(u.date_created),
                        'date_modified': str(u.date_modified),
                        'banned': u.banned}), 201
    else:
        return jsonify({'message': 'username is already esist'}), 422

@blueprint.route('/<int:user_id>', methods=['POST', 'PATCH'])
@limiter.limit("60/minute")
def user_patch(user_id):
    """修改用户信息"""
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
        raise

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
        raise

@blueprint.route('/scope')
def scope_get():
    scope = Scope.query.all()
    items = []
    for i in scope:
        items.append({'id': i.id, 'name': i.name})
    return jsonify({'total_count': len(items), 'items': items}), 200


