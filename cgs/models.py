# -*- coding: utf-8 -*-
import json

from peewee import *

from app import db, mysql_db


class BaseModel(Model):
    
    @classmethod
    def get_one(cls, *query, **kwargs):
        # 为了方便使用，新增此接口，查询不到返回None，而不抛出异常
        try:
            return cls.get(*query, **kwargs)
        except DoesNotExist:
            return None

class JSONModel(BaseModel):
    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        return str(r)

class Users(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    date_created = DateTimeField()
    date_modified = DateTimeField()
    banned = BooleanField(default=False)

    class Meta:
        database = db

class Vehicle_gd(BaseModel):
    hpzl = CharField()
    hphm = CharField()
    clpp1 = CharField()
    clxh = CharField()
    clpp2 = CharField()
    gcjk = CharField()
    zzg = CharField()
    zzcmc = CharField()
    clsbdh = CharField()
    fdjh = CharField()
    cllx = CharField()
    csys = CharField()
    sfzmhm = CharField()
    sfzmmc = CharField()
    syr = CharField()
    fzrq = CharField()
    class Meta:
        database = mysql_db

