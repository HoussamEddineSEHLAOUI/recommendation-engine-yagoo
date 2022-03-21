

from pymongo import MongoClient
import environement


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
    print('Collection names :', db.list_collection_names())
    return db


def get_collection(name_collection):
    return get_database()[name_collection]


def get_tags():
    print('START PRINTING TAGS CATEGORY')
    l = {}
    i = 0
    print(get_collection('tags').find_one())
    for x in get_collection('tags').find():
        l[i] = x['category']
        i = i+1
    return l


def get_recommendation():
    l = {}
    i = 0
    for x in get_collection('recommendation').find():
        l[i] = x['title']
        i = i+1
        break
    return l
