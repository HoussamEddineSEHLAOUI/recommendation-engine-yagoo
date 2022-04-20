
import environement
import pandas as pd
import pymongo


class Database(object):
    URI = environement.URL_DATA_BASE
    DATABASE_NAME = environement.DATA_BASE_NAME
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client[Database.DATABASE_NAME]

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)