# -*- coding: utf-8 -*-
import arrow
from flask import g, request
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, app, api, auth, limiter, logger
from models import Users


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
    decorators = [limiter.limit("50/minute")]

    def get(self):
        return {'user_url': 'http://127.0.0.1:%s/v1/hbc' %
                app.config['PORT']}, 200,
        {'Cache-Control': 'public, max-age=60, s-maxage=60'}


class UserList(Resource):
    decorators = [limiter.limit("50/hour")]

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


api.add_resource(Index, '/')
api.add_resource(UserList, '/user')
api.add_resource(TokenList, '/token')
