import pandas as pd
from datetime import datetime

NAME = 'c6'

def uploadBills(csv_file_path, control_collection):
    file_date = extract_date(csv_file_path)
    document = control_collection.find_one({'file_date': file_date})
    if document:
        print(f'[WARN] File from bank_name {NAME} and date {file_date} already exists')
        return
    return read_csv(csv_file_path, file_date)

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

def read_csv(csv_file_path, file_date):
    df = pd.read_csv(csv_file_path, sep=';')
    data = df.to_dict(orient='records')
    document = {
        "file_date" : file_date,
        "data" : data
    }
    return document

