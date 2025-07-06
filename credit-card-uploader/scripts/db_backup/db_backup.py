import datetime, os, subprocess, firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv

load_dotenv()
db_uri = os.getenv("DB_URI")
db_name = os.getenv("DB_NAME")
firebase_bucket_name = os.getenv("FIREBASE_BUCKET_NAME")

def create_mongo_dump():
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    dump_name = f"backup-credit_card_reader-mongo-{date_str}.gz"

    command = [
        "mongodump",
        f"--uri={db_uri}/{db_name}",
        f"--archive={dump_name}",
        "--gzip"
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Backup created: {dump_name}")
        return dump_name
    except subprocess.CalledProcessError as e:
        print(f"Error creating backup: {e}")
        return None

def upload_to_firebase(file_path):
    if not firebase_admin._apps:
        cred = credentials.Certificate("../../data/creds/serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': firebase_bucket_name
        })

    bucket = storage.bucket()
    blob = bucket.blob(f"backups/credit-card-reader-mongo/{file_path}")
    blob.upload_from_filename(file_path)
    print(f"Upload finished: backups/{file_path}")

def delete_local_file(file_path):
    try:
        os.remove(file_path)
        print(f"Local file deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting local file: {e}")

if __name__ == "__main__":
    dump_file = create_mongo_dump()
    if dump_file:
        upload_to_firebase(dump_file)
        delete_local_file(dump_file)
