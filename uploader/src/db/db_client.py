import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("DB_URI")
MONGO_DABATASE = os.getenv("DB_NAME")

COLLECTION_UPLOADS = 'uploads'
COLLECTION_TAGS = 'tags'


def db_connect():
    print('Oppening connection to database...')
    mongo_client = MongoClient(MONGO_URI)
    return mongo_client[MONGO_DABATASE]


# Insert queries

def db_file_data_insert(bank_name, tmp_file_name, file_date, file_data):
    collection_data = dbClient[bank_name]
    collection_data.insert_one(file_data)
    
    dbClient[COLLECTION_UPLOADS].insert_one({
                    'file_name': tmp_file_name,
                    'bank_name': collection_data.name,
                    'file_date': file_date,
                    'upload_date': datetime.now()
                })
    
    print(f'[INFO] Data saved to database!')


def db_insert_tags(tags, hash, name):
    collection_data = dbClient[COLLECTION_TAGS]
    collection_data.insert_many(tags)

    dbClient[COLLECTION_UPLOADS].insert_one({
                    'file_name': name,
                    'hash': hash,
                    'upload_date': datetime.now()
                })
    
    print(f'[INFO] Tags saved to database!')


# Find queries

def db_find_uploaded_data_by_name_and_bank(bank_name, tmp_file_name):
    return dbClient[COLLECTION_UPLOADS].find_one({'file_name': tmp_file_name, 'bank_name': bank_name})

def db_find_uploaded_data_by_name(tmp_file_name):
    return dbClient[COLLECTION_UPLOADS].find_one({'file_name': tmp_file_name})


# Drop collections

def db_drop_all_collections():
    dbClient[COLLECTION_UPLOADS].drop()
    dbClient[COLLECTION_TAGS].drop()
    dbClient['c6'].drop()
    print(f'[INFO] All collections dropped')


def db_drop_collection(collection_name):
    dbClient[collection_name].drop()
    print(f'[INFO] Collection {collection_name} dropped')


dbClient = db_connect()
