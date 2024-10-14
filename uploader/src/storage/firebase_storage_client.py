import firebase_admin
import os
from dotenv import load_dotenv
from firebase_admin import credentials, storage

load_dotenv()

firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
firebase_bucket_name = os.getenv("FIREBASE_BUCKET_NAME")

def connect():
    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred, {
        "storageBucket": firebase_bucket_name
    })

    return storage.bucket()

def list_pending_files_to_process():
    files = []
    blobs = client.list_blobs(prefix="bills/")
    for blob in blobs:
        if blob.name.endswith(".csv"):
            files.append(blob.name)
    return files

def download_file(remote_path, local_path):
    local_path = f"data/tmp_files/{local_path}"
    blob = client.blob(remote_path)
    blob.download_to_filename(local_path)
    print(f"File {remote_path} downlaoded to {local_path} with success.")

client = connect()
