#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from base import BaseModel, Base

class RegisteredUser(Base, BaseModel):
    __tablename__ = 'registered_user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
       return "<Registered User('%s','%s')>" % (self.name, self.email)


