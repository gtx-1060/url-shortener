from datetime import datetime, timedelta
from sqlalchemy import Column, Text, Boolean, Enum, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.data.db.db import Base
from app.dtos.privacy_modes import PrivacyModes


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(Text, nullable=False)
    password = Column(Text, default=False)
    url_statistics = relationship("Statistics", backref=backref("owner", cascade="all, delete"), passive_deletes=True)


class Configuration(Base):
    __tablename__ = 'configuration'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    privacy = Column(Enum(PrivacyModes), default=PrivacyModes.PRIVATE)
    bots_protect = Column(Boolean, default=False)
    live_until_date = Column(TIMESTAMP, default=datetime.now()+timedelta(days=30))
    live_until_visits = Column(Integer, nullable=True)
    url_id = Column(Integer, ForeignKey('url.id', ondelete='CASCADE'), nullable=False)


class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    visits = Column(Integer, default=0)
    last_visit = Column(TIMESTAMP, default=datetime.now())
    creation = Column(TIMESTAMP, default=datetime.now())
    owner_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    url_id = Column(Integer, ForeignKey('url.id', ondelete='CASCADE'),  nullable=False)


class Url(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    original_url = Column(Text, nullable=False)
    shorted_url = Column(Text, nullable=False)
    configuration = relationship('Configuration', passive_deletes=True)
    statistics = relationship('Statistics', passive_deletes=True)
