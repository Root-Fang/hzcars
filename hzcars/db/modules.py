# -*- coding: utf-8 -*-

"""
  Author: FangPengdong
  Date: 2017/1/4 16:49
  Description:
  
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, CHAR
from sqlalchemy.sql import func

Base = declarative_base()

class Mixin(object):
    def __init__(self, **kwargs):
        super(Mixin, self).__init__()
        for key,val in kwargs.items():
            if hasattr(self.__class__, key) and not key.startswith("_"):
                if type(val) == unicode:
                    self.__dict__[key] = val.encode("utf-8")
                else:
                    self.__dict__[key] = val

class CompetitionResult(Mixin, Base):
    __tablename__ = 'competition_result'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_bin'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_time = Column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())
    updated_time = Column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())
    month = Column(CHAR(7), nullable=False, default="0000-00", unique=True, index=True)
    personal_participate_total = Column(Integer, nullable=False)
    personal_total = Column(Integer, nullable=False)
    personal_avg_price = Column(Integer, nullable=False)
    personal_min_price = Column(Integer, nullable=False)
    personal_min_price_volume = Column(Integer)
    personal_min_price_total = Column(Integer)
    corporate_participate_total = Column(Integer, nullable=False)
    corporate_total = Column(Integer, nullable=False)
    corporate_avg_price = Column(Integer, nullable=False)
    corporate_min_price = Column(Integer, nullable=False)
    corporate_min_price_volume = Column(Integer)
    corporate_min_price_total = Column(Integer)

    def __init__(self, **kwargs):
        super(CompetitionResult, self).__init__(**kwargs)

class LotteryResult(Mixin, Base):
    __tablename__ = 'lottery_result'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_bin'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_time = Column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())
    updated_time = Column(DateTime(timezone=True), nullable=False, server_default=func.current_timestamp())
    month = Column(CHAR(7), nullable=False, default="0000-00", unique=True, index=True)
    personal_participate_total = Column(Integer, nullable=False)
    personal_total = Column(Integer, nullable=False)
    corporate_participate_total = Column(Integer, nullable=False)
    corporate_total = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        super(LotteryResult, self).__init__(**kwargs)

    dict()

