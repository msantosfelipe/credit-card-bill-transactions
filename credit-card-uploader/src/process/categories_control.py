import db.db_client as db_client
import hashlib
import json
import os

CATEGORIES_FILE_PATH = os.environ.get("CATEGORIES_FILE_PATH")
CATEGORIES_AI_FILE_PATH = os.environ.get("CATEGORIES_AI_FILE_PATH")


def upload_categories():
    hash = _generate_categories_file_hash()
    category_control = db_client.db_find_category_control()

    if category_control is None:
        _insert_categories(hash)
        return
    else:
        if category_control['hash'] == hash:
            print(f'[INFO] Categories have not been updated, skipping reimport')
            return
        else:
            print(f'[WARN] Categories have been updated, dropping categories collection to be reimported!')
            db_client.db_clean_categories()
            _insert_categories(hash)
    

def remove_categories_ai_file():
    if os.path.exists(CATEGORIES_AI_FILE_PATH):
        os.remove(CATEGORIES_AI_FILE_PATH)        


def _insert_categories(hash):
    all_categories = []

    if os.path.exists(CATEGORIES_FILE_PATH):
        with open(CATEGORIES_FILE_PATH, "r") as file:
            categories = json.load(file)
            all_categories.extend(categories)

    if os.path.exists(CATEGORIES_AI_FILE_PATH):
        with open(CATEGORIES_AI_FILE_PATH, "r") as ai_file:
            ai_categories = json.load(ai_file)
            all_categories.extend(ai_categories)
    
    if len(all_categories) > 0:
        db_client.db_insert_categories(all_categories, hash)


def _generate_categories_file_hash():
    hash_categories_file = ""
    hash_categories_ai_file = ""
    
    if os.path.exists(CATEGORIES_FILE_PATH):
        with open(CATEGORIES_FILE_PATH, "rb") as file:
            content = file.read()
            hash_categories_file = hashlib.sha256(content).hexdigest()

    if os.path.exists(CATEGORIES_AI_FILE_PATH):
        with open(CATEGORIES_AI_FILE_PATH, "rb") as file:
            content = file.read()
            hash_categories_ai_file = hashlib.sha256(content).hexdigest()

    combined_hash = hash_categories_file + hash_categories_ai_file
    return hashlib.sha256(combined_hash.encode()).hexdigest()
