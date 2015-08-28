# -*- coding: utf-8 -*-
import datetime
import json

import arrow
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

def send_get(url,headers = {'content-type': 'application/json'}):
    """POST请求"""
    r = requests.get(url, headers=headers,
                     auth=HTTPDigestAuth('kakou', 'pingworker'))

    return r

def auth_test(url):
    headers = {'Authorization': 'Digest kakou="pingworker"',
               'content-type': 'application/json'}
    r = requests.get(url, headers=headers)

    return r

def user_test():
    auth = HTTPBasicAuth('admin', 'showmethemoney')
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:8098/user'
    data = {'username': 'fire19', 'password': 'show me the money',
            'scope': 'vehicle'}
    r = requests.post(url, headers=headers,data=json.dumps(data),auth=auth)

    return r

def token_test():
    #auth = HTTPBasicAuth('admin','gdsx27677221')
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:8098/token'
    data = {'username': 'admin', 'password': 'showmethemoney'}
    r = requests.post(url, headers=headers, data=json.dumps(data))

    return r

def vehicle_test():
    url = 'http://localhost:8098/vehicle?q=粤WJV023+hpys:blue'
    headers = {'content-type': 'application/json',
               'access_token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MDc4MTM4MCwiaWF0IjoxNDQwNzc3NzgwfQ.eyJzY29wZSI6bnVsbCwidWlkIjo0fQ.HGqB_ZC9RG8L28sD4adhCZ1iFh5Q8V0mNgdY42Ol80I'}
    r = requests.get(url, headers=headers)
    return r

def user_get():
    url = 'http://localhost:8098/user/1'
    headers = {'content-type': 'application/json',
               'access_token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MDc5NDY0NCwiaWF0IjoxNDQwNzkxMDQ0fQ.eyJzY29wZSI6WyJhbGwiXSwidWlkIjoxfQ.XLC4POsheL3MSUnxyKiMgzytcCSZ_1YV1PPTk8pVad8'}
    r = requests.get(url, headers=headers)
    return r

def user_post():
    headers = {'content-type': 'application/json',
               'access_token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MDc5NDY0NCwiaWF0IjoxNDQwNzkxMDQ0fQ.eyJzY29wZSI6WyJhbGwiXSwidWlkIjoxfQ.XLC4POsheL3MSUnxyKiMgzytcCSZ_1YV1PPTk8pVad8'}
    url = 'http://127.0.0.1:8098/user'
    data = {'username': 'fire20', 'password': 'test12345', 'scope': 'scope_get'}
    r = requests.post(url, headers=headers,data=json.dumps(data))

    return r

def user_put():
    headers = {'content-type': 'application/json',
               'access_token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MDc5NDY0NCwiaWF0IjoxNDQwNzkxMDQ0fQ.eyJzY29wZSI6WyJhbGwiXSwidWlkIjoxfQ.XLC4POsheL3MSUnxyKiMgzytcCSZ_1YV1PPTk8pVad8'}
    url = 'http://127.0.0.1:8098/user/4'
    data = {'scope': 'scope_get,user_get'}
    r = requests.put(url, headers=headers, data=json.dumps(data))

    return r

def scope_get():
    url = 'http://localhost:8098/scope'
    headers = {'content-type': 'application/json',
               'access_token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MDc4MTM4MCwiaWF0IjoxNDQwNzc3NzgwfQ.eyJzY29wZSI6bnVsbCwidWlkIjo0fQ.HGqB_ZC9RG8L28sD4adhCZ1iFh5Q8V0mNgdY42Ol80I'}
    r = requests.get(url, headers=headers)
    return r

if __name__ == '__main__':  # pragma nocover
    r = user_put()
    #r = scope_get()
    print r.headers
    #r = auth_test(url)
    print r.status_code
    print r.text
