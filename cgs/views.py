# -*- coding: utf-8 -*-
import urlparse
import urllib
from functools import wraps

import arrow
from flask import g, request
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, app, api, auth, limiter, cache, logger, access_logger
from models import Users, Scope, VehicleGD, Hbc_all, HZ_vehicle
from help_func import *


@app.after_request
def after_request(response):
    """访问信息写入日志"""
    access_logger.info('%s - - [%s] "%s %s HTTP/1.1" %s %s'
                       % (request.remote_addr,
                          arrow.now().format('DD/MMM/YYYY:HH:mm:ss ZZ'),
                          request.method, request.path, response.status_code,
                          response.content_length))
    return response

def verify_addr(f):
    """IP地址白名单"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not app.config['WHITE_LIST_OPEN'] or request.remote_addr in app.config['WHITE_LIST']:
            pass
        else:
            return {'status': '403.6',
                    'error': u'禁止访问:客户端的 IP 地址被拒绝'}, 403
        return f(*args, **kwargs)
    return decorated_function

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
        print 'scope'
        try:
            scope = '_'.join([request.path[1:], request.method.lower()])
            print scope
        except Exception as e:
            print (e)
        if 'all' in g.scope or scope in g.scope:
            pass
        else:
            return {'status': 405, 'error': 'Method Not Allowed'}, 405
        return f(*args, **kwargs)
    return decorated_function

@cache.memoize(3600)
def get_vehicle(hphm='', hpys=None):
    vehicle = VehicleGD.query.filter_by(hphm=hphm)
    if hpys:
        hpzl = []
        if hpys in set([u'blue', u'蓝', u'2']):
            hpzl = ('02', '08')
        elif hpys in set([u'yellow', u'黄', u'3']):
            hpzl = ('01', '07', '13', '14', '15', '16', '17')
        elif hpys in set([u'white',u'白',u'4']):
            hpzl = ('20', '21', '22', '24', '32')
        elif hpys in set([u'black',u'黑',u'5']):
            hpzl = ('03', '04', '05', '06', '09', '10', '11', '12')
        else:
            hpzl = ()
        vehicle = VehicleGD.query.filter(VehicleGD.hpzl.in_(hpzl))
    return vehicle.all()

@cache.memoize(3600)
def get_hbc(hphm='', hpzl='00'):
    v = HZ_vehicle.query.outerjoin(Hbc_all, HZ_vehicle.xh==Hbc_all.nxh).filter(HZ_vehicle.hphm==hphm, HZ_vehicle.hphm==Hbc_all.hphm, HZ_vehicle.hpzl==hpzl).first()

    return v


class Index(Resource):

    def get(self):
        help(request)
        return {
            'user_url': 'http://%s:%s/user{/user_id}' % (request.remote_addr, app.config['PORT']),
            'scope_url': 'http://%s:%s/scope' % (request.remote_addr, app.config['PORT']),
            'token_url': 'http://%s:%s/token' % (request.remote_addr, app.config['PORT']),
            'vehicle_url': 'http://%s:%s/vehicle' % (request.remote_addr, app.config['PORT']),
            'hzhbc_url': 'http://%s:%s/hzhbc/:hphm/:hpzl' % (request.remote_addr, app.config['PORT'])
        }, 200, {'Cache-Control': 'public, max-age=60, s-maxage=60'}


class User(Resource):
    decorators = [verify_token, limiter.limit("50/minute")]

    @verify_addr
    @verify_scope
    def get(self, user_id):
        user = Users.query.filter_by(id=user_id, banned=0).first()
        if user:
            return {'id': user.id,
                    'username': user.username,
                    'scope': user.scope,
                    'date_created': str(user.date_created),
                    'date_modified': str(user.date_modified),
                    'banned': user.banned}, 200
        else:
            return {}, 404

    @verify_addr
    @verify_scope
    def put(self, user_id):
        verify_scope('user_put')
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

        db.session.query(Users).filter_by(id=user_id).update({'scope': u_scope, 'date_modified': arrow.now().datetime})
        db.session.commit()

        user = Users.query.filter_by(id=user_id).first()
        app.config['SCOPE_USER'][user.id] = set(user.scope.split(','))

        return {
            'id': user.id,
            'username': user.username,
            'scope': user.scope,
            'date_created': str(user.date_created),
            'date_modified': str(user.date_modified),
            'banned': user.banned
        }, 201


class UserList(Resource):
    decorators = [verify_token, limiter.limit("50/minute")]

    @verify_addr
    @verify_scope
    def post(self):
        verify_scope('user_post')
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
            # 求交集后的权限
            u_scope = ','.join(all_scope & request_scope)
            u = Users(username=request.json['username'],
                      password=password_hash, scope=u_scope, banned=0)
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


class ScopeList(Resource):

    @verify_addr
    @verify_token
    @verify_scope
    def get(self):
        scope = Scope.query.all()
        items = []
        for i in scope:
            items.append(row2dict(i))
        return {'total_count': len(items), 'items': items}, 200


def get_uid():
    user = Users.query.filter_by(username=request.json.get('username', ''),
                                 banned=0).first()
    g.uid = -1
    if user:
        if sha256_crypt.verify(request.json.get('password', ''), user.password):
            g.uid = user.id
            g.scope = user.scope
    return str(g.uid)


class TokenList(Resource):
    decorators = [limiter.limit("5/hour", get_uid), verify_addr]

    def post(self):
        #verify_scope('token_post')
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


class Vehicle(Resource):
    decorators = [limiter.limit("500/minute")]

    @verify_addr
    @verify_token
    #@verify_scope
    def get(self):
        parse_result = urlparse.urlparse(request.url)
        query = urllib.unquote(parse_result.query)
        get_params = url_decode(query)

        if not get_params.get('q', None):
            error = {'resource': 'Search', 'field': 'q', 'code': 'missing'}
            return {'message': 'Validation Failed', 'error': error}, 422
        q_dict = q_decode(get_params['q'])

        vehicle = get_vehicle(q_dict['q'], q_dict.get('hpys', None))

        items = []
        for i in vehicle:
            items.append({'id': i.id, 'hpzl': i.hpzl, 'clxh': i.clxh,
                          'clpp1': i.clpp1, 'clpp2': i.clpp2, 'zzcmc': i.zzcmc,
                          'clsbdh': i.clsbdh, 'fdjh': i.fdjh, 'cllx': i.cllx,
                          'csys': i.csys, 'syr': i.syr, 'fzrq': i.fzrq})

        return {'total_count': len(items), 'items': items}, 200,
        {'Cache-Control': 'public, max-age=60, s-maxage=60'}


class HZHbc(Resource):
    decorators = [limiter.limit("6000/minute")]

    @verify_addr
    @verify_token
    #@verify_scope
    def get(self, hphm, hpzl):
        try:
            hbc = get_hbc(hphm, hpzl)
            item = {}
            if hbc:
                item = row2dict(hbc)
        except Exception as e:
            print (e)
        return item, 200,
        {'Cache-Control': 'public, max-age=60, s-maxage=60'}


api.add_resource(Index, '/')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/user')
api.add_resource(ScopeList, '/scope')
api.add_resource(TokenList, '/token')
api.add_resource(Vehicle, '/vehicle')
api.add_resource(HZHbc, '/hzhbc/<string:hphm>/<string:hpzl>')
