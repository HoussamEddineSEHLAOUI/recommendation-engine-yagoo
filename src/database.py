from bson.objectid import ObjectId
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

    def convert_to_dataFrame(collection, query):
        # Make a query to the specific DB and Collection
        cursor = Database.find(collection, query)

        # convert alll objectId to string,
        ListWithoutOId = map(lambda row: {i: str(row[i]) if isinstance(
            row[i], ObjectId) else row[i] for i in row}, cursor)

        # Expand the cursor and construct the DataFrame
        dataframe = pd.DataFrame(list(cursor))
        return dataframe
