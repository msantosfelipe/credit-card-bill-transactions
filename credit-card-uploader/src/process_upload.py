import os
import shutil
from db import db_helper
import process_tag
from banks.c6 import process_upload_c6
from datetime import datetime

input_folder = "src/input/"
output_folder = "src/processed/"
c6 = 'c6'

def process_files_in_directory(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.csv'):
                csv_file_path = os.path.join(root, filename)
                bank_name = os.path.basename(os.path.dirname(csv_file_path))
                read_csv_and_insert_mongodb(bank_name, csv_file_path)
                #move_processed_file(csv_file_path)  # UNCOMMENT THIS LINE
    print('[INFO] All files uploaded!')

def read_csv_and_insert_mongodb(bank_name, csv_file_path):
    print(f'**************************************')
    print(f'[INFO] Processing file {csv_file_path}')
    dbClient = db_helper.getDbClient()
    collection = dbClient[bank_name]
    control_collection = dbClient[db_helper.mongo_collection_uploads]
    file_date = None
    
    if bank_name == process_upload_c6.NAME:
        # C6 csv upload
        file_date = process_upload_c6.extract_date(csv_file_path)
        result = process_upload_c6.uploadBills(csv_file_path, control_collection)

    else:
        print(f'[ERROR] Invalid bank_name: {bank_name}')
        return None

    insertOnDb(collection, control_collection, csv_file_path, file_date, result)
    process_tag.process_tag_from_upload(bank_name, collection, process_tag.getTags(dbClient), file_date)
    print(f'[INFO] Data from {csv_file_path} successfully processed!')

def insertOnDb(collection, control_collection, csv_file_path, file_date, result):
    collection.insert_one(result)
    control_collection.insert_one({
                    'file_name': csv_file_path,
                    'bank_name': collection.name,
                    'file_date': file_date,
                    'upload_date': datetime.now()
                })
    print(f'[INFO] Data saved to database!')

def move_processed_file(file_path):
    filename = os.path.basename(file_path)
    destination_path = os.path.join(output_folder, filename)
    shutil.move(file_path, destination_path)
    print(f'[INFO] File moved to: {destination_path}')

if __name__ == '__main__':
    process_files_in_directory(input_folder)
