import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("DB_URI")
mongo_database = os.getenv("DB_NAME")

collection_uploads = 'uploads'
#mongo_collection_tags = 'tags'


def db_connect():
    print('executing db_connect')
    mongo_client = MongoClient(mongo_uri)
    return mongo_client[mongo_database]


def db_file_data_insert(bank_name, tmp_file_name, file_date, file_data):
    collection_data = dbClient[bank_name]
    collection_data.insert_one(file_data)
    
    dbClient[collection_uploads].insert_one({
                    'file_name': tmp_file_name,
                    'bank_name': collection_data.name,
                    'file_date': file_date,
                    'upload_date': datetime.now()
                })
    print(f'[INFO] Data saved to database!')


def db_find_uploaded_data_by_name(bank_name, tmp_file_name):
    return dbClient[collection_uploads].find_one({'file_name': tmp_file_name, 'bank_name': bank_name})


dbClient = db_connect()
