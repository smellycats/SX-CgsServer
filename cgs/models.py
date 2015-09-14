# -*- coding: utf-8 -*-
import arrow

from app import db


class Users(db.Model):
    """用户"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True)
    password = db.Column(db.String(128))
    scope = db.Column(db.String(128), default='')
    date_created = db.Column(db.DateTime, default=arrow.now().datetime)
    date_modified = db.Column(db.DateTime, default=arrow.now().datetime)
    banned = db.Column(db.Integer, default=0)

    def __init__(self, username, password, scope='', banned=0,
                 date_created=None, date_modified=None):
        self.username = username
        self.password = password
        self.scope = scope
        now = arrow.now().datetime
        if not date_created:
            self.date_created = now
        if not date_modified:
            self.date_modified = now
        self.banned = banned

    def __repr__(self):
        return '<Users %r>' % self.id


class Scope(db.Model):
    """权限范围"""
    __tablename__ = 'scope'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Scope %r>' % self.id


class Csys(db.Model):
    """车身颜色"""
    __bind_key__ = 'cgs'
    __tablename__ = 'csys'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(1), unique=True)
    name = db.Column(db.String(3), index=False)

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<Csys %r>' % self.id


class VehicleGD(db.Model):
    """车管所数据"""
    __bind_key__ = 'cgs'
    __tablename__ = 'vehicle_gd'
    id = db.Column(db.Integer, primary_key=True)
    hpzl = db.Column(db.String(2))
    hphm = db.Column(db.String(16))
    clpp1 = db.Column(db.String(32))
    clxh = db.Column(db.String(64))
    clpp2 = db.Column(db.String(64))
    gcjk = db.Column(db.String(4))
    zzg = db.Column(db.String(32))
    zzcmc = db.Column(db.String(128))
    clsbdh = db.Column(db.String(128))
    fdjh = db.Column(db.String(64))
    cllx = db.Column(db.String(3))
    csys = db.Column(db.String(4))
    sfzmhm = db.Column(db.String(32))
    sfzmmc = db.Column(db.String(8))
    syr = db.Column(db.String(128))
    fzrq = db.Column(db.String(32))

    def __init__(self, hpzl, hphm, clpp1, clxh, clpp2, gcjk, zzg, zzcmc,
                 clsbdh, fdjh, cllx, csys, sfzmhm, sfzmmc, syr, fzrq):
        self.hpzl = hpzl
        self.hphm = hphm
        self.clpp1 = clpp1
        self.clxh = clxh
        self.clpp2 = hphm
        self.gcjk = hphm
        self.zzg = hphm
        self.zzcmc = hphm
        self.clsbdh = clsbdh
        self.fdjh = fdjh
        self.cllx = cllx
        self.csys = csys
        self.sfzmhm = sfzmhm
        self.sfzmmc = sfzmmc
        self.syr = syr
        self.fzrq = fzrq

    def __repr__(self):
        return '<VehicleGD %r>' % self.id


class HbcAll(db.Model):
    __bind_key__ = 'hbc'
    __tablename__ = 'hbc_all'
    id = db.Column(db.Integer, primary_key=True)
    nxh = db.Column(db.String(32))
    hphm = db.Column(db.String(16))
    hpzl = db.Column(db.String(2))

    def __init__(self, nxh, hphm, hpzl):
        self.nxh = nxh
        self.hphm = hphm
        self.hpzl = hpzl

    def __repr__(self):
        return '<HbcAll %r>' % self.nxh


class HZVehicle(db.Model):
    __bind_key__ = 'hbc'
    __tablename__ = 'hz_vehicle'
    id = db.Column(db.Integer, primary_key=True)
    xh = db.Column(db.String(32))
    hphm = db.Column(db.String(16))
    hpzl = db.Column(db.String(2))

    def __init__(self, xh, hphm, hpzl):
        self.xh = xh
        self.hphm = hphm
        self.hpzl = hpzl

    def __repr__(self):
        return '<HZVehicle %r>' % self.xh
