from pymongo import MongoClient
from datetime import datetime
import os
import pandas as pd
import shutil

mongo_uri = 'mongodb://localhost:27017/'
mongo_database = 'credit_card_reader_mongo'
mongo_control_collection = 'uploads'

input_folder = "src/input/"
output_folder = "src/processed/"

def read_csv_and_insert_mongodb(bank, csv_file_path):
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client[mongo_database]
    collection = db[bank]
    control_collection = db[mongo_control_collection]

    file_date = extract_date(csv_file_path)

    document = control_collection.find_one({'file_date': file_date})

    if document:
        print('[WARN] File from bank', bank, 'and date', file_date, 'already exists')
        return
    
    result = read_c6(csv_file_path, file_date)

    collection.insert_one(result)

    control_collection.insert_one({
                    'file_name': csv_file_path,
                    'bank': collection.name,
                    'file_date': file_date,
                    'import_date': datetime.now()
                })
    
    print('[INFO] Data from', csv_file_path, 'imported to MongoDB!')

def read_c6(csv_file_path, file_date):
    df = pd.read_csv(csv_file_path, sep=';')
    data = df.to_dict(orient='records')
    document = {file_date: data}
    return document

def extract_date(csv_file_path):
    try:
        date = csv_file_path.split('_')[1].split('.csv')[0]
        date_object = datetime.strptime(date, '%Y-%m-%d')
        month = date_object.strftime('%m')
        year = date_object.year
        return f'{year}-{month}'
    except Exception as e:
        print(f'[ERROR] Failed extracting date: {e}')
        return None

def process_files_in_directory(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.csv'):
                csv_file_path = os.path.join(root, filename)
                bank = os.path.basename(os.path.dirname(csv_file_path))
                read_csv_and_insert_mongodb(bank, csv_file_path)
                move_file(csv_file_path)
    print('[INFO] All files imported!')

def move_file(file_path):
    filename = os.path.basename(file_path)
    destination_path = os.path.join(output_folder, filename)
    shutil.move(file_path, destination_path)
    print("File moved to:", destination_path)

if __name__ == '__main__':
    process_files_in_directory(input_folder)
