from pymongo import MongoClient

def connect(uri: str = 'mongodb://localhost:27017/', db_name: str = 'smart_home'):
    client = MongoClient(uri)
    return client[db_name]
