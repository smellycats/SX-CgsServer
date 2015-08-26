# -*- coding: utf-8 -*-
import urllib


def url_decode(query):
    d = {}
    params_list = query.split('&')
    for i in params_list:
        if i.find('=') >= 0:
            k,v = i.split('=', 1)
            d[k] = v
    return d

def q_decode(q):
    d = {}
    q_list = q.split('+')
    d['q'] = q_list[0]
    for i in q_list[1:]:
        if i.find(':') >= 0:
            k,v = i.split(':', 1)
            d[k] = v
    return d

if __name__ == "__main__":
    #s = get_hpzl(u'粤L12345', 5)
    #print s[0], s[1]
    #print urldecode(u'q%3D粤L12=34%2Bhpzl:02+cllx:K31%26order=desc')
    query = 'q'
    print url_decode(query);
    #q = u'\u7ca4L12=34+hpzl:02+cllx:K31'
    #print q_decode(q)

