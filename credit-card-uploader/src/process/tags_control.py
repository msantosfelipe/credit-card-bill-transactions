import db.db_client as db_client
import hashlib
import json
import os

TAGS_FILE_PATH = os.environ.get("TAGS_FILE_PATH")


def upload_tags():
    hash = _generate_tags_file_hash()

    tag_control = db_client.db_find_tag_control()
    if tag_control is None:
        _insert_tags(hash)
        return
    else:
        if tag_control['hash'] == hash:
            print(f'[INFO] Tags have not been updated, skipping reimport')
            return
        else:
            print(f'[WARN] Tags have been updated, dropping tags collection to be reimported!')
            db_client.db_clean_tags()
            _insert_tags(hash)
    

def _insert_tags(hash):
    with open(TAGS_FILE_PATH, "r") as file:
        tags = json.load(file)
        db_client.db_insert_tags(tags, hash)


def _generate_tags_file_hash():
    with open(TAGS_FILE_PATH, "rb") as file:
        content = file.read()
        hash_obj = hashlib.sha256(content)
        hash_hex = hash_obj.hexdigest()
    return hash_hex
