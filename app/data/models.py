from datetime import datetime, timedelta
from sqlalchemy import Column, Text, Boolean, Enum, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.data.db.db import SyncBase as Base
from app.dtos.privacy_modes import PrivacyModes


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, default=False)
    # statistics of all created urls
    url_statistics = relationship("Statistics", backref=backref("owner", cascade="all, delete"), passive_deletes=True)


class Configuration(Base):
    __tablename__ = 'configuration'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # specifies who gets access to the url stats
    privacy = Column(Enum(PrivacyModes), default=PrivacyModes.PRIVATE)
    bots_protect = Column(Boolean, default=False)
    # specifies the date of the url destroying
    # default = 30 days
    live_until_date = Column(TIMESTAMP, default=datetime.now()+timedelta(days=30))
    # specifies the number of visits for destroying the url
    live_until_visits = Column(Integer, nullable=True)
    # parent url id
    url_id = Column(Integer, ForeignKey('url.id', ondelete='CASCADE'), nullable=False)


class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # number of visits url
    visits = Column(Integer, default=0)
    # datetime of last visit
    last_visit = Column(TIMESTAMP, default=datetime.now())
    # url creation datetime
    creation = Column(TIMESTAMP, default=datetime.now())
    owner_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    # parent url id
    url_id = Column(Integer, ForeignKey('url.id', ondelete='CASCADE'),  nullable=False)


class Url(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    original_url = Column(Text, nullable=False)
    # only hash without domain and etc
    shorted_url = Column(Text, nullable=False, index=True, unique=True)
    # configuration with additional url options
    configuration = relationship('Configuration', passive_deletes=True)
    # url statistics (actually visits and dates)
    statistics = relationship('Statistics', backref=backref('url', cascade="all, delete"), passive_deletes=True)
