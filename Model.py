#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,backref
from sqlalchemy import create_engine

from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape

from geojson import Feature

Base = declarative_base()


class OSMNode(Base):
    __tablename__ = 'osm_nodes'
    id = Column(Integer, primary_key=True)
    osm_id = Column(BigInteger)
    name = Column(String(250))
    location = Column(Geometry('POINT'))


class Dumpster(Base):
    __tablename__ = 'dumpsters'
    id = Column(Integer, primary_key=True)

    osmnode = relationship(OSMNode, backref=backref("dumpsters", uselist=False))
    osmnode_id = Column(Integer, ForeignKey('osm_nodes.id'))

    def count_upvotes(self):
        i=0
        for vote in self.votes:
            if vote.value==1:
                i+=1
        return i
    def count_downvotes(self):
        i=0
        for vote in self.votes:
            if vote.value==-1:
                i+=1
        return i
    def __geojson__(self):
        properties = {'id': self.id, 'name': self.osmnode.name, 'upvotes': self.count_upvotes(), 'downvotes': self.count_downvotes(), 'osmnode_id': self.osmnode.osm_id }
        geometry = to_shape(self.osmnode.location)
        feature = Feature(geometry=geometry, properties=properties)
        return feature

    def __unicode__(self):
        return self.__str__()
    def __str__(self):
        return self.osmnode.name


class Session(Base):
    # Represents a user session
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    ip = Column(String(250))

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    created = Column(DateTime)

    dumpster = relationship(Dumpster, backref='votes')
    dumpster_id = Column(Integer, ForeignKey('dumpsters.id'))

    session = relationship(Session, backref='votes')
    session_id = Column(Integer, ForeignKey('sessions.id'))

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    comment = Column(String(500))
    created = Column(DateTime)

    dumpster = relationship(Dumpster, backref='comments')
    dumpster_id = Column(Integer, ForeignKey('dumpsters.id'))

    session = relationship(Session, backref='comments')
    session_id = Column(Integer, ForeignKey('sessions.id'))

