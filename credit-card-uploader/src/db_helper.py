from pymongo import MongoClient

mongo_uri = 'mongodb://localhost:27017/'
mongo_database = 'credit_card_reader_mongo'
mongo_upload_collection = 'uploads'

def getCollection(bank):
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client[mongo_database]
    return db[bank]