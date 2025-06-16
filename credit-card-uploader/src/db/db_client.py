import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("DB_URI")
MONGO_DABATASE = os.getenv("DB_NAME")

CATEGORY_CONTROL_NAME = "category_control"

COLLECTION_UPLOADS = 'uploads'
COLLECTION_BILLS = 'bills'
COLLECTION_CATEGORIES = 'categories'


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
                    'bank_name': bank_name,
                    'file_date': file_date,
                    'import_date': datetime.now(),
                    'upload_date': datetime.now()
                })
    
    print(f'[INFO] Data saved to database!')


def db_insert_categories(categories, hash):
    collection_data = db_client[COLLECTION_CATEGORIES]
    collection_data.insert_many(categories)
    db_client[COLLECTION_UPLOADS].insert_one({
                    'file_name': CATEGORY_CONTROL_NAME,
                    'hash': hash,
                    'upload_date': datetime.now()
                })
    print(f'[INFO] Categories saved to database!')


def db_append_ai_category(category, description):
    db_category = db_client[COLLECTION_CATEGORIES].find_one({'name': category})
    if db_category is None:
        db_client[COLLECTION_CATEGORIES].insert_one({
            "name" : category,
            "keyworkds" : [description]
        })
        return
    

def db_update_categories_hash(hash):
    db_client[COLLECTION_UPLOADS].update_one(
        {'file_name': CATEGORY_CONTROL_NAME},
        {
            '$set': {
                'hash': hash,
            }
        }
    )


def db_update_bill(file_date, bank, data):
    db_client[COLLECTION_BILLS].update_one(
        {'file_date': file_date, 'bank': bank},
        {
            '$set': {
                'data': data,
            }
        }
    )


# Find queries

def db_find_all_bills():
    return db_client[COLLECTION_BILLS].find()


def db_find_uploaded_data_by_name_and_bank(bank_name, tmp_file_name):
    return db_client[COLLECTION_UPLOADS].find_one({'file_name': tmp_file_name, 'bank_name': bank_name})


def db_find_category_control():
    return db_client[COLLECTION_UPLOADS].find_one({'file_name': CATEGORY_CONTROL_NAME})


def db_find_categories():
    categories_data = db_client[COLLECTION_CATEGORIES].find({}, {"_id": 0})
    categories_dict = {}

    for category_data in categories_data:
        name = category_data["name"]
        keywords = category_data["keywords"]
        categories_dict[name] = keywords
    
    return categories_dict


# Drop collections

def db_clean_categories():
    db_client[COLLECTION_CATEGORIES].drop()
    db_client[COLLECTION_UPLOADS].delete_one({'file_name': CATEGORY_CONTROL_NAME})


def db_drop_all_collections():
    db_client[COLLECTION_UPLOADS].drop()
    db_client[COLLECTION_BILLS].drop()
    db_client[COLLECTION_CATEGORIES].drop()
    db_client['raw_c6'].drop()
    db_client['raw_xp'].drop()
    print(f'[WARN] All collections dropped')


db_client = _db_connect()
