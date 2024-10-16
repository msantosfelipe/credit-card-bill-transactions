from db.db_client import db_find_uploaded_data_by_name, db_insert_tags, db_drop_all_collections
import hashlib
import json

TAG_CONTROL_NAME = 'tag_control'
TAGS_FILE_PATH = 'data/tags.json'


def upload_tags():
    hash = generate_tags_file_hash()

    tag_control = get_tag_control()
    if tag_control is None:
        insert_tags(hash)
        return
    else:
        if tag_control['hash'] == hash:
            print(f'[INFO] Tags have not been updated, skipping reimport')
            return
        else:
            print(f'[WARN] Tags have been updated, dropping all collections to be reimported!')
            db_drop_all_collections()
            insert_tags(hash)
    

def insert_tags(hash):
    with open(TAGS_FILE_PATH, "r") as file:
        tags = json.load(file)
        db_insert_tags(tags, hash, TAG_CONTROL_NAME)


def get_tag_control():
    return db_find_uploaded_data_by_name(TAG_CONTROL_NAME)


def generate_tags_file_hash():
    with open(TAGS_FILE_PATH, "rb") as file:
        content = file.read()
        hash_obj = hashlib.sha256(content)
        hash_hex = hash_obj.hexdigest()
    return hash_hex
