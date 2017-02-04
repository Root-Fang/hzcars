# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
from hzcars.db.modules import Base, CompetitionResult
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
import logging, os


db_session = None

def getSession(path=None, echo=True, forced=False):
    global db_session
    if forced or db_session is None:
        if path is None or path == "":
            raise DropItem("Missing DB_PATH")
        engine = create_engine(path, encoding = "utf-8", echo = echo)
        db_session = scoped_session(sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, autocommit=True))
        Base.query = db_session.query_property()
        Base.metadata.create_all(bind=engine)
        return db_session
    else:
        return db_session


class HzcarsPipeline(object):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.path = kwargs["DB_PATH"]
        self.echo = kwargs["SQL_ECHO"]

    def process_item(self, item, spider):
        if item is None or 'month' not in item or item['month'] is None or len(item['month']) == 0:
            self.logger.error("Missing Month")
            raise DropItem("Missing Month")
        if 'table' not in item or item['table'] is None or item['table'] == '':
            self.logger.error("Please provide table")
            raise DropItem("Missing table")
        session = getSession(path=self.path, echo=self.echo)
        table = item['table']
        try:
            record = session.query(table).filter_by(month = item['month'].encode("utf-8")).one()
        except Exception as e:
            tmp = dict(item)
            del tmp['table']
            tmp['created_time'] = datetime.now()
            tmp['updated_time'] = tmp['created_time']
            tmp = table(**tmp)
            session.begin()
            try:
                session.add(tmp)
                session.commit()
            except Exception as e:
                self.logger.error(e, exc_info=True)
                session.rollback()
                raise DropItem("Database Failed")
            else:
                return item
        else:
            tmp = dict(item)
            del tmp['table']
            dirty = False
            for key,value in tmp.items():
                if key != "id" and hasattr(record, key) and not key.startswith("_"):
                    value = value if type(value) != unicode else value.encode("utf-8")
                    if value != str(getattr(record, key)):
                        setattr(record, key, value)
                        dirty = True
            if dirty:
                setattr(record, 'updated_time', datetime.now())
                session.begin()
                try:
                    session.add(record)
                    session.commit()
                except Exception as e:
                    self.logger.error(e, exc_info=True)
                    session.rollback()
                    raise DropItem("Can't Update the Database")
                else:
                    return item
            else:
                return item


    @classmethod
    def from_crawler(cls, crawler):
        kwargs = dict()
        kwargs["SQL_ECHO"] = crawler.settings["SQL_ECHO"]
        kwargs["DB_PATH"] = crawler.settings["DB_PATH"]
        o = cls(**kwargs)
        return o


    def close_spider(self, spider):
        self.logger.info("Invoke the close_spider which belong to %s", spider.name)
        global db_session
        if db_session is not None:
            session = getSession()
            session.remove()