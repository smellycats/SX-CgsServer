# -*- coding: utf-8 -*-
from cgs import db

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
        return '<Csys %r>' % self.code


class GDVehicle(db.Model):
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
        return '<GDVehicle %r>' % self.id


