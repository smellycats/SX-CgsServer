# -*- coding: utf-8 -*-
from datetime import datetime
import urlparse
import urllib
from functools import wraps

from flask import g, request
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, app, api, auth, limiter, logger
from models import Users, VehicleGD, Scope
from help_func import *


@auth.verify_password
def verify_password(username, password):
    if username.lower() == 'admin':
        user = Users.query.filter_by(username='admin').first()
    else:
        return False
    if user:
        return sha256_crypt.verify(password, user.password)
    return False

def verify_token(f):
    """token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Access-Token'):
            return {'error': 'access_token error'}, 401
        token_result = verify_auth_token(request.headers['Access-Token'],
                                         app.config['SECRET_KEY'])
        if not token_result:
            return {'error': 'access_token invalid'}, 401
        elif token_result == 'expired':
            return {'error': 'access_token expired'}, 401
        g.uid = token_result['uid']
        g.scope = set(token_result['scope'])

        return f(*args, **kwargs)
    return decorated_function


class Index(Resource):
    def get(self):
        return {
            'user_url': 'http://127.0.0.1:%s/user{/username}' %  app.config['PORT'],
            'scope_url': 'http://127.0.0.1:%s/scope' %  app.config['PORT'],
            'token_url': 'http://127.0.0.1:%s/token' %  app.config['PORT'],
            'vehicle_url': 'http://127.0.0.1:%s/vehicle' %  app.config['PORT']
        }, 200, {'Cache-Control': 'public, max-age=60, s-maxage=60'}


class User(Resource):
    decorators = [limiter.limit("50/minute")]

    @verify_token
    def get(self, user_id):
        if not 'user_get' in g.scope and not 'all' in g.scope:
            return {'error': 'Method Not Allowed'}, 405
        user = Users.query.filter_by(id=user_id, banned=0).first()
        if user:
            return {'id': user.id,
                    'username': user.username,
                    'scope': user.scope,
                    'date_created': str(user.date_created),
                    'date_modified': str(user.date_modified)}, 200
        else:
            return {}, 404

    @verify_token
    def put(self, user_id):
        if not 'user_put' in g.scope and not 'all' in g.scope:
            return {'error': 'Method Not Allowed'}, 405
        parser = reqparse.RequestParser()

        parser.add_argument('scope', type=unicode, required=True,
                            help='A scope field is require', location='json')
        args = parser.parse_args()

        # 所有权限范围
        all_scope = set()
        for i in Scope.query.all():
            all_scope.add(i.name)
        # 授予的权限范围
        request_scope = set(request.json.get('scope', u'null').split(','))
        # 求交集后的权限
        u_scope = ','.join(all_scope & request_scope)

        db.session.query(Users).filter_by(id=user_id).update({'scope': u_scope, 'date_modified': datetime.now()})
        db.session.commit()

        user = Users.query.filter_by(id=user_id).first()
        app.config['SCOPE_USER'][user.id] = set(user.scope.split(','))

        return {'id': user.id,
                'username': user.username,
                'scope': user.scope,
                'date_created': str(user.date_created),
                'date_modified': str(user.date_modified),
                'banned': user.banned}, 201    


class UserList(Resource):
    decorators = [limiter.limit("50/minute")]

    @verify_token
    def post(self):
        if not 'user_post' in g.scope and not 'all' in g.scope:
            return {'error': 'Method Not Allowed'}, 405
        parser = reqparse.RequestParser()

        parser.add_argument('username', type=unicode, required=True,
                            help='A username field is require', location='json')
        parser.add_argument('password', type=unicode, required=True,
                            help='A password field is require', location='json')
        args = parser.parse_args()

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
            # 求交集后的权限
            u_scope = ','.join(all_scope & request_scope)
            u = Users(username=request.json['username'],
                      password=password_hash, scope=u_scope, banned=0)
            db.session.add(u)
            db.session.commit()
            return {'id': u.id,
                    'username': u.username,
                    'scope': u.scope,
                    'date_created': str(u.date_created),
                    'date_modified': str(u.date_modified),
                    'banned': u.banned}, 201
        else:
            return {'error': 'username is already esist'}, 422


class ScopeList(Resource):

    @verify_token
    def get(self):
        if not 'scope_get' in g.scope and not 'all' in g.scope:
            return {'error': 'Method Not Allowed'}, 405
        scope = Scope.query.all()
        items = []
        for i in scope:
            items.append(row2dict(i))
        return {'total_count': len(items), 'items': items}, 200


class TokenList(Resource):
    decorators = [limiter.limit("5/hour")]
    
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('username', type=unicode, required=True,
                            help='A username field is require', location='json')
        parser.add_argument('password', type=unicode, required=True,
                            help='A password field is require', location='json')
        args = parser.parse_args()

        user = Users.query.filter_by(username=request.json['username'],
                                     banned=0).first()
        if user:
            if sha256_crypt.verify(request.json['password'], user.password):
                s = Serializer(app.config['SECRET_KEY'],
                               expires_in=app.config['EXPIRES'])

                token = s.dumps({'uid': user.id,
                                 'scope': user.scope.split(',')})

                return {'access_token': token, 'uid': user.id,
                        'token_type': 'self', 'scope': user.scope,
                        'expires_in': app.config['EXPIRES']}, 200,
                {'Cache-Control': 'no-store', 'Pragma': 'no-cache'}

        return {'error': 'username or password error'}, 422


class Vehicle(Resource):
    decorators = [limiter.limit("500/minute")]

    @verify_token
    def get(self):
        parse_result = urlparse.urlparse(request.url)
        query = urllib.unquote(parse_result.query)
        get_params = url_decode(query)

        if not get_params.get('q', None):
            error = {'resource': 'Search', 'field': 'q', 'code': 'missing'}
            return {'message': 'Validation Failed', 'error': error}, 422
        q_dict = q_decode(get_params['q'])

        vehicle = VehicleGD.query.filter_by(hphm=q_dict['q'])
        if q_dict.get('hpys', None):
            hpzl = []
            if q_dict['hpys'] in set([u'blue', u'蓝', u'2']):
                hpzl = ('02', '08')
            elif q_dict['hpys'] in set([u'yellow', u'黄', u'3']):
                hpzl = ('01', '07', '13', '14', '15', '16', '17')
            elif q_dict['hpys'] in set([u'white',u'白',u'4']):
                hpzl = ('20', '21', '22', '24', '32')
            elif q_dict['hpys'] in set([u'black',u'黑',u'5']):
                hpzl = ('03', '04', '05', '06', '09', '10', '11', '12')
            else:
                hpzl = ()
            vehicle = VehicleGD.query.filter(VehicleGD.hpzl.in_(hpzl))

        items = []
        for i in vehicle.all():
            items.append({'id': i.id, 'hpzl': i.hpzl, 'clxh': i.clxh,
                          'clpp1': i.clpp1, 'clpp2': i.clpp2, 'zzcmc': i.zzcmc,
                          'clsbdh': i.clsbdh, 'fdjh': i.fdjh, 'cllx': i.cllx,
                          'csys': i.csys, 'syr': i.syr, 'fzrq': i.fzrq})

        return {'total_count': len(items), 'items': items}, 200,
        {'Cache-Control': 'public, max-age=60, s-maxage=60'}



api.add_resource(Index, '/')
api.add_resource(User, '/user/<user_id>')
api.add_resource(UserList, '/user')
api.add_resource(ScopeList, '/scope')
api.add_resource(TokenList, '/token')
api.add_resource(Vehicle, '/vehicle')
