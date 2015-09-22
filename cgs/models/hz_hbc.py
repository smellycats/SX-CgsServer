# -*- coding: utf-8 -*-
from cgs import db

class HbcAll(db.Model):
    __bind_key__ = 'cgs'
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
    __bind_key__ = 'cgs'
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
