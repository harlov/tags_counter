# -*- coding: utf-8 -*-
# pylint: disable=C0103

"""
Создание подключения к монго
"""

from tags_counter import app
from pymongo import MongoClient


class Mongo(object):
    def __init__(self):
        self.mongo_connection = None
        self.db = None

    def get_db(self):
        if self.db is not None:
            return self.db
        self.db = self.get_connection()[app.config['MONGODB_NAME']]
        print 'MONGO CONNECT %s' % (app.config['MONGODB_NAME'], )
        return self.db

    def get_connection(self):
        if self.mongo_connection is not None:
            return self.mongo_connection

        self.mongo_connection = MongoClient(host=app.config['MONGODB_HOST'],
                                            port=app.config['MONGODB_PORT'],
                                            connect=False)
        return self.mongo_connection

mongo = Mongo()
