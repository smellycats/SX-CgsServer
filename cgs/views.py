# -*- coding: utf-8 -*-
import urlparse
import urllib

import arrow
from flask import g, request
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from playhouse.shortcuts import model_to_dict

from app import db, app, api, auth, limiter, logger
from models import Users, Vehicle_gd
from help_func import url_decode, q_decode


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@auth.verify_password
def verify_password(username, password):
    if username.lower() == 'admin':
        user = Users.get_one(Users.username == 'admin')
    else:
        return False
    if user:
        return sha256_crypt.verify(password, user.password)
    return False


class Index(Resource):
    def get(self):
        return {'user_url': 'http://127.0.0.1:%s/v1/hbc' %
                app.config['PORT']}, 200,
        {'Cache-Control': 'public, max-age=60, s-maxage=60'}


class UserList(Resource):
    decorators = [limiter.limit("60/minute")]

    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('username', type=unicode, required=True,
                            help='A username field is require', location='json')
        parser.add_argument('password', type=unicode, required=True,
                            help='A password field is require', location='json')
        args = parser.parse_args()

        user = Users.get_one(Users.username == request.json['username'],
                             Users.banned == False)
        if not user:
            now = str(arrow.now())
            password_hash = sha256_crypt.encrypt(request.json['password'],
                                                 rounds=app.config['ROUNDS'])
            Users.create(username=request.json['username'],
                         password=password_hash,
                         date_created=now,
                         date_modified=now,
                         banned=False)
            _id = 0
            for i in Users.raw('SELECT last_insert_rowid() AS id'):
                _id = i.id
            return {'username': request.json['username'],
                    'id': _id, 'date_created': now}, 201
        else:
            return {'error': 'username is already esist'}, 422


class TokenList(Resource):
    decorators = [limiter.limit("5/hour")]

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('username', type=unicode, required=True,
                            help='A username field is require', location='json')
        parser.add_argument('password', type=unicode, required=True,
                            help='A password field is require', location='json')
        args = parser.parse_args()

        user = Users.get_one(Users.username == request.json['username'],
                             Users.banned == False)

        if user:
            if sha256_crypt.verify(request.json['password'], user.password):
                s = Serializer(app.config['SECRET_KEY'],
                               expires_in=app.config['EXPIRES'])
                token = s.dumps({'uid': user.id})
                return {'access_token': token, 'uid': user.id,
                        'expires_in': app.config['EXPIRES']}, 201

        return {'error': 'username or password error'}, 422


class Vehicle(Resource):

    def get(self):
        parse_result = urlparse.urlparse(request.url)
        query = urllib.unquote(parse_result.query)
        get_params = url_decode(query)

        if not get_params.get('q', None):
            error = {'resource': 'Search', 'field': 'q', 'code': 'missing'}
            return {'message': 'Validation Failed', 'error': error}, 422
        q_dict = q_decode(get_params['q'])
        vehicle = (Vehicle_gd
                   .select()
                   .where(Vehicle_gd.hphm == q_dict['q']))

        if q_dict.get('hpys', None):
            hpzl = []
            if q_dict['hpys'] in set([u'blue', u'蓝', u'2']):
                hpzl = ['02', '08']
            elif q_dict['hpys'] in set([u'yellow', u'黄', u'3']):
                hpzl = ['01', '07', '13', '14', '15', '16', '17']
            elif q_dict['hpys'] in set([u'white',u'白',u'4']):
                hpzl = ['20', '21', '22', '24', '32']
            elif q_dict['hpys'] in set([u'black',u'黑',u'5']):
                hpzl = ['03', '04', '05', '06', '09', '10', '11', '12']
            else:
                hpzl = []
            vehicle = vehicle.where(Vehicle_gd.hpzl << hpzl)
        items = []
        for i in vehicle:
            items.append({'id': i.id,
                          'hpzl': i.hpzl,
                          'clxh': i.clxh,
                          'clpp1': i.clpp1,
                          'clpp2': i.clpp2,
                          'zzcmc': i.zzcmc,
                          'clsbdh': i.clsbdh,
                          'fdjh': i.fdjh,
                          'cllx': i.cllx,
                          'csys': i.csys,
                          'syr': i.syr,
                          'fzrq': i.fzrq})

        return {'total_count': len(items), 'items': items}, 200,
        {'Cache-Control': 'public, max-age=60, s-maxage=60'}


api.add_resource(Index, '/')
api.add_resource(UserList, '/user')
api.add_resource(TokenList, '/token')
api.add_resource(Vehicle, '/vehicle')
