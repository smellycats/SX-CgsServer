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
    auth = HTTPBasicAuth('admin', 'gdsx27677221')
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:8098/user'
    data = {'username': 'fire4', 'password': 'show me the money'}
    r = requests.post(url, headers=headers,data=json.dumps(data),auth=auth)

    return r

def token_test():
    #auth = HTTPBasicAuth('admin','gdsx27677221')
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:8098/token'
    data = {'username': 'fire4', 'password': 'show me the money'}
    r = requests.post(url, headers=headers, data=json.dumps(data))

    return r

if __name__ == '__main__':  # pragma nocover
    r = token_test()
    print r.headers
    #r = auth_test(url)
    print r.status_code
    print r.text
