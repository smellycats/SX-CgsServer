# -*- coding: utf-8 -*-

from peewee import *

from app import db


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_one(cls, *query, **kwargs):
        # 为了方便使用，新增此接口，查询不到返回None，而不抛出异常
        try:
            return cls.get(*query, **kwargs)
        except DoesNotExist:
            return None


class Users(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    date_created = DateTimeField()
    date_modified = DateTimeField()
    banned = BooleanField(default=False)
