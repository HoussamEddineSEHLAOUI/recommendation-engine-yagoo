

from pymongo import MongoClient
import environement
import pandas as pd
from bson.objectid import ObjectId


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    HOST_DB = environement.HOST_DB
    PORT_DB = environement.PORT_DB
    USER_NAME_DB = environement.USER_NAME_DB
    PASSWORD_DB = environement.PASSWORD_DB
    DATA_BASE_NAME = environement.DATA_BASE_NAME
    AUTH_MECHANISM = environement.AUTH_MECHANISM

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    # client = pymongo.MongoClient(HOST, int(PORT))
    # client = pymongo.MongoClient(CONNECTION_STRING)
    # print(client)
    client = MongoClient(HOST_DB,
                         username=USER_NAME_DB,
                         password=PASSWORD_DB,
                         port=int(PORT_DB),
                         authMechanism=AUTH_MECHANISM
                         )

    db = client[DATA_BASE_NAME]
    print(db.list_collection_names())
    return db


def get_collection(name_collection):
    # Get collection by name :
    return get_database()[name_collection]


def get_dataFrame(name_collection):
    # Make a query to the specific DB and Collection
    cursor = get_collection(name_collection).find()

    # convert alll objectId to string,
    ListWithoutOId = map(lambda row: {i: str(row[i]) if isinstance(
        row[i], ObjectId) else row[i] for i in row}, cursor)

    # Expand the cursor and construct the DataFrame
    dataframe = pd.DataFrame(list(ListWithoutOId)[:3])
    return dataframe


def get_Tags_DataFrame():
    return get_dataFrame('tags')


def get_Recommendation_DataFrame():
    return get_dataFrame('recommendation')
