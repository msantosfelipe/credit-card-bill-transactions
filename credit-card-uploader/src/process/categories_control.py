import db.db_client as db_client
import hashlib
import json
import os
from collections import defaultdict

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
            print(f'[WARN] Categories have been updated, dropping categories collection and reimporting!')
            db_client.db_clean_categories()
            _insert_categories(hash)


def update_hash():
    hash = _generate_categories_file_hash()
    db_client.db_update_categories_hash(hash)

def remove_categories_ai_file():
    if os.path.exists(CATEGORIES_AI_FILE_PATH):
        os.remove(CATEGORIES_AI_FILE_PATH)        


def _insert_categories(hash):
    print("[INFO] Inserting categories")
    merged_categories = defaultdict(set)
    if os.path.exists(CATEGORIES_FILE_PATH):
        with open(CATEGORIES_FILE_PATH, "r") as file:
            categories = json.load(file)
            for cat in categories:
                merged_categories[cat['name']].update(cat.get('keywords', []))

    if os.path.exists(CATEGORIES_AI_FILE_PATH):
        with open(CATEGORIES_AI_FILE_PATH, "r") as ai_file:
            ai_categories = json.load(ai_file)
            for cat in ai_categories:
                merged_categories[cat['name']].update(cat.get('keywords', []))

    all_categories = [
        {"name": name, "keywords": sorted(list(keywords))}
        for name, keywords in merged_categories.items()
    ]

    if all_categories:
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
