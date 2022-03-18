

from pymongo import MongoClient


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    USER8NAME = 'root'
    PASSSWORD = 'T8GRF2_uB4/?qCvq'
    PORT = '29517'
    HOST = '149.202.107.243'
    DATA_BASE_NAME = 'yaago-staging'

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    # client = pymongo.MongoClient(HOST, int(PORT))
    # client = pymongo.MongoClient(CONNECTION_STRING)
    # print(client)
    client = MongoClient(HOST,
                         username=USER8NAME,
                         password=PASSSWORD,
                         authMechanism='MONGODB-CR')
    db = client[DATA_BASE_NAME]
    return db


def get_collection(name_collection):
    return get_database()[name_collection]
