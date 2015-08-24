#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ConfigParser import ConfigParser

class Store():
    def __init__(self, db_connection):

        engine = create_engine(db_connection)

        # Nur beim ersten Mal
        Base.metadata.create_all(engine)

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def get_all(self, model):
        return self.session.query(model).all()

    def get_first(self, model, **kwargs):
        return self.get(model, **kwargs)

    def get(self, model, **kwargs):
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            return None

    def exists(self, model, **kwargs):
        # Returns: object, is_new
        # get_or_create(db, Account, username=username, password=password)
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            return True
        else:
            return False

    def get_or_create(self, model, **kwargs):
        # Returns: object, is_new
        # get_or_create(db, Account, username=username, password=password)
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            instance = model(**kwargs)
            self.session.add(instance)
            self.session.commit()
            return instance, True

    def delete_if_exists(self, model, **kwargs):
        # Returns: True if found and deleted, else False
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        else:
            return False
