# -*- coding: utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


def url_decode(query):
    d = {}
    params_list = query.split('&')
    for i in params_list:
        if i.find('=') >= 0:
            k, v = i.split('=', 1)
            d[k] = v
    return d


def q_decode(q):
    d = {}
    q_list = q.split('+')
    d['q'] = q_list[0]
    for i in q_list[1:]:
        if i.find(':') >= 0:
            k, v = i.split(':', 1)
            d[k] = v
    return d


def verify_auth_token(token, key):
    s = Serializer(key)
    try:
        return s.loads(token)
    except SignatureExpired:
        # valid token, but expired
        return 'expired'
    except BadSignature:
        # invalid token
        return None


def row2dict(row):
    d = {}
    for col in row.__table__.columns:
        d[col.name] = getattr(row, col.name)
    return d
