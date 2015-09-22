# -*- coding: utf-8 -*-
import datetime
import json

import arrow
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

IP = '127.0.0.1'
PORT = 5000

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
    data = {'username': 'fire4', 'password': 'showmethemoney',
            'scope': 'vehicle'}
    r = requests.post(url, headers=headers,data=json.dumps(data),auth=auth)

    return r

def token_test():
    #auth = HTTPBasicAuth('admin','gdsx27677221')
    headers = {'content-type': 'application/json'}
    url = 'http://%s:%s/token' % (IP, PORT)
    data = {'username': 'test1', 'password': 'test12345'}
    r = requests.post(url, headers=headers, data=json.dumps(data))

    return r

def vehicle_test():
    url = 'http://localhost:8098/vehicle?q=粤WJV023+hpys:blue'
    headers = {'content-type': 'application/json',
               'access_token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MDc4MTM4MCwiaWF0IjoxNDQwNzc3NzgwfQ.eyJzY29wZSI6bnVsbCwidWlkIjo0fQ.HGqB_ZC9RG8L28sD4adhCZ1iFh5Q8V0mNgdY42Ol80I'}
    r = requests.get(url, headers=headers)
    return r

def user_get(token):
    url = 'http://localhost:8098/user/1'
    headers = {'content-type': 'application/json',
               'access_token': token}
    r = requests.get(url, headers=headers)
    return r

def user_post():
    headers = {'content-type': 'application/json',
               'access_token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MDc5NDY0NCwiaWF0IjoxNDQwNzkxMDQ0fQ.eyJzY29wZSI6WyJhbGwiXSwidWlkIjoxfQ.XLC4POsheL3MSUnxyKiMgzytcCSZ_1YV1PPTk8pVad8'}
    url = 'http://127.0.0.1:8098/user'
    data = {'username': 'test2', 'password': 'test12345', 'scope': 'all'}
    r = requests.post(url, headers=headers,data=json.dumps(data))

    return r

def user_put():
    headers = {'content-type': 'application/json',
               'access_token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MDc5NDY0NCwiaWF0IjoxNDQwNzkxMDQ0fQ.eyJzY29wZSI6WyJhbGwiXSwidWlkIjoxfQ.XLC4POsheL3MSUnxyKiMgzytcCSZ_1YV1PPTk8pVad8'}
    url = 'http://127.0.0.1:8098/user/4'
    data = {'scope': 'scope_get,user_get'}
    r = requests.put(url, headers=headers, data=json.dumps(data))

    return r

def scope_get(token):
    url = 'http://localhost:5000/scope/'
    headers = {'content-type': 'application/json',
               'access_token': token}
    r = requests.get(url, headers=headers)
    return r

def hzhbc_get(token):
    hphm = 'LC6879'
    hpzl = '02'
    url = 'http://192.168.1.29:8081/hzhbc/%s/%s' % (hphm, hpzl)
    headers = {'content-type': 'application/json', 'access_token': token}
    r = requests.get(url, headers=headers)
    return r

def hzhbcall_get(token):
    url = 'http://%s:%s/hzhbc' % (IP, PORT)
    headers = {'content-type': 'application/json', 'access_token': token}
    return requests.get(url, headers=headers)

def gdvehicle_get(token):
    url = 'http://%s:%s/gdvehicle/粤WJV023/blue' % (IP, PORT)
    headers = {'content-type': 'application/json', 'access_token': token}
    return requests.get(url, headers=headers)

if __name__ == '__main__':  # pragma nocover
    token = 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0Mjk1MjY1MCwiaWF0IjoxNDQyOTQ1NDUwfQ.eyJzY29wZSI6WyJnZHZlaGljbGVfZ2V0IiwiaHpoYmNfZ2V0Il0sInVpZCI6Mn0.UcuOOUusLVmpawjPH8RPKDqfoAQSMFxfKZoX7Mqtyas'
    r = token_test()
    r = hzhbcall_get(token)
    #r = gdvehicle_get(token)
    #r = scope_get()
    print r.headers
    print r.status_code
    #print r.text
    #print r.text[:20]
