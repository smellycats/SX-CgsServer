# -*- coding: utf-8 -*-
from app import db
from models import Users
import datetime
#from requests_func import RequestsFunc


def model_test():
    db.connect()

    #Package.create(timeflag=123, ip='127.0.0.1', path='my/path')
    Hbc.insert(jgsj=datetime.datetime.now(),hphm='粤L12345',kkdd_id='345',hpys_id=2,fxbh_id=4,cdbh=5,imgurl='httP;//123',imgpath='c:123',banned=True).execute()
    query = Hbc.raw("SELECT LAST_INSERT_ID() AS id")
    #print help(query)
    #print query.id
    for i in query:
        print i.id
        break
    db.close()

def model_test():
    db.connect()

    Users.create_table()
    db.close()


if __name__ == '__main__':
    #model_test()
    #conf_test()
    #log_test()
    model_test()
    #flask_run_test()
