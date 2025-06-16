import db.db_client as db_client
import hashlib
import json
import os

CATEGORIES_FILE_PATH = os.environ.get("CATEGORIES_FILE_PATH")


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
    

def _insert_categories(hash):
    with open(CATEGORIES_FILE_PATH, "r") as file:
        categories = json.load(file)
        db_client.db_insert_categories(categories, hash)


def _generate_categories_file_hash():
    with open(CATEGORIES_FILE_PATH, "rb") as file:
        content = file.read()
        hash_obj = hashlib.sha256(content)
        hash_hex = hash_obj.hexdigest()
    return hash_hex
