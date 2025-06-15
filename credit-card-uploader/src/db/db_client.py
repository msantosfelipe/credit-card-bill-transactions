import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("DB_URI")
MONGO_DABATASE = os.getenv("DB_NAME")

TAG_CONTROL_NAME = 'tag_control'

COLLECTION_UPLOADS = 'uploads'
COLLECTION_BILLS = 'bills'
COLLECTION_TAGS = 'tags'


def _db_connect():
    print('Oppening connection to database...')
    mongo_client = MongoClient(MONGO_URI)
    return mongo_client[MONGO_DABATASE]


# Insert queries

def db_file_data_insert(bank_name, tmp_file_name, file_date, file_data, bill):
    collection_data = db_client[f"raw_{bank_name}"]
    collection_data.insert_one(file_data)

    collection_transaction = db_client[COLLECTION_BILLS]
    collection_transaction.insert_one(bill)

    db_client[COLLECTION_UPLOADS].insert_one({
                    'file_name': tmp_file_name,
                    'bank_name': collection_data.name,
                    'file_date': file_date,
                    'import_date': datetime.now(),
                    'upload_date': datetime.now()
                })
    
    print(f'[INFO] Data saved to database!')


def db_insert_tags(tags, hash):
    collection_data = db_client[COLLECTION_TAGS]
    collection_data.insert_many(tags)

    db_client[COLLECTION_UPLOADS].insert_one({
                    'file_name': TAG_CONTROL_NAME,
                    'hash': hash,
                    'upload_date': datetime.now()
                })
    
    print(f'[INFO] Tags saved to database!')


def db_update_bill(file_date, bank, data):
    db_client[COLLECTION_BILLS].update_one(
        {'file_date': file_date, 'bank': bank},
        {
            '$set': {
                'data': data,
            }
        },
    )


# Find queries

def db_find_all_bills():
    return db_client[COLLECTION_BILLS].find()

def db_find_uploaded_data_by_name_and_bank(bank_name, tmp_file_name):
    return db_client[COLLECTION_UPLOADS].find_one({'file_name': tmp_file_name, 'bank_name': bank_name})


def db_find_tag_control():
    return db_client[COLLECTION_UPLOADS].find_one({'file_name': TAG_CONTROL_NAME})


def db_find_tags():
    tags_data = db_client[COLLECTION_TAGS].find({}, {"_id": 0})
    tags_dict = {}

    for tag_data in tags_data:
        name = tag_data["name"]
        keywords = tag_data["keywords"]
        tags_dict[name] = keywords
    
    return tags_dict


# Drop collections

def db_clean_tags():
    db_client[COLLECTION_TAGS].drop()
    db_client[COLLECTION_UPLOADS].delete_one({'file_name': TAG_CONTROL_NAME})

def db_drop_all_collections():
    db_client[COLLECTION_UPLOADS].drop()
    db_client[COLLECTION_BILLS].drop()
    db_client[COLLECTION_TAGS].drop()
    db_client['raw_c6'].drop()
    db_client['raw_xp'].drop()
    print(f'[WARN] All collections dropped')


db_client = _db_connect()
