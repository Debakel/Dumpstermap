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
import json
Base = declarative_base()


class OSMNode(Base):
    __tablename__ = 'osm_nodes'
    id = Column(Integer, primary_key=True)
    osm_id = Column(BigInteger)
    name = Column(String(250))
    location = Column(Geometry('POINT'))

    city = Column(String(250))
    street = Column(String(250))
    housenumber = Column(String(50))

class Dumpster(Base):
    __tablename__ = 'dumpsters'
    id = Column(Integer, primary_key=True)

    osmnode = relationship(OSMNode, backref=backref("dumpsters", uselist=False))
    osmnode_id = Column(Integer, ForeignKey('osm_nodes.id'))

    @property
    def voting(self):
        return self.upvotes - self.downvotes

    @property
    def upvotes(self):
        i=0
        for vote in self.votes:
            if vote.value==1:
                i+=1
        return i

    @property
    def downvotes(self):
        i=0
        for vote in self.votes:
            if vote.value==-1:
                i+=1
        return i
    def __geojson__(self):
        comments = []
        for comment in self.comments:
            comments.append(comment.to_dict())
        color = 'grey'
        if self.upvotes > self.downvotes:
            color = 'green'
        elif self.upvotes < self.downvotes:
            color = 'red'
        properties = {'id': self.id,
                      'name': self.osmnode.name,
                      'addr:street': self.osmnode.street,
                      'addr:housenumber': self.osmnode.housenumber,
                      'addr:city': self.osmnode.city,
                      'upvotes': self.upvotes,
                      'downvotes': self.downvotes,
                      'osmnode_id': self.osmnode.osm_id,
                      'comments': comments,
                      'total_votes': self.upvotes - self.downvotes,
                      'good': self.upvotes > self.downvotes,
                      'not_good': self.upvotes < self.downvotes,
                      'color': color
                      }
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
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'comment': self.comment, 'dumpster_id': self.dumpster_id, 'date': '?' }
    def __json__(self):
        return json.dumps(self.to_dict())