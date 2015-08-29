# -*- coding: utf-8 -*-
#from requests_func import RequestsFunc
import datetime

from ini_conf import MyIni
from cgs import db
from cgs.models import Users, Scope, VehicleGD


def ini_test():
    myini = MyIni()
    try:
        print myini.get_kakou()
        print myini.get_hbc()
        print myini.get_mysql()
        print myini.get_syst()
    except ConfigParser.NoOptionError as e:
        print e

def model_test2():
    db.connect()

    #Package.create(timeflag=123, ip='127.0.0.1', path='my/path')
    Hbc.insert(jgsj=datetime.datetime.now(),hphm='粤L12345',kkdd_id='345',
               hpys_id=2,fxbh_id=4,cdbh=5,imgurl='httP;//123',imgpath='c:123',
               banned=True).execute()
    query = Hbc.raw("SELECT LAST_INSERT_ID() AS id")
    #print help(query)
    #print query.id
    for i in query:
        print i.id
        break
    db.close()

def model_test():
    vehicle = VehicleGD.query.all()
    print vehicle

def get_test():
    q = VehicleGD.query.filter_by(hphm='粤WJV023')
    r = q.filter_by(hpzl='06').all()
    #r = q.all()
    #v = db.session.query(Vehicle_gd).filter_by(hpzl='02').first()
    #db.session.commit()
    print r

def user_add():
    user = Users(username='admin3', password='password', scope='user_get')
    db.session.add(user)
    db.session.commit()
    print user.id

def users_test():
    user = Users(username='admin3', password='password', scope='jack')
    db.session.add(user)
    db.session.commit()
    print user.id

def users_get():
    q = Users.query.all()
    print q

def users_get2():
    q = Users.query.filter_by(id=3, banned=0).first()
    print q

def users_get():
    q = Users.query.all()
    print q

def scope_get():
    q = Scope.query.filter(Scope.id.in_((1,2))).all()
    #help(Scope.query.filter)
    print q

def scope_set():
    db.session.query(Scope).filter_by(id=5).update({'name': 'test4'})
    db.session.commit()
    print scope

def cache_test():
    q = VehicleGD
    print q

if __name__ == '__main__':
    #model_test()
    #conf_test()
    #log_test()
    #users_test()
    #flask_run_test()
    #users_get()
    #users_test()
    #scope_get()
    #scope_set()
    user_add()

