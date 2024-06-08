from pymongo import MongoClient

mongo_uri = 'mongodb://localhost:27017/'
mongo_database = 'credit_card_reader_mongo'
mongo_collection_uploads = 'uploads'
mongo_collection_tags = 'tags'
mongo_collection_c6 = 'c6'

def getDbClient():
    mongo_client = MongoClient(mongo_uri)
    return mongo_client[mongo_database]