# Process CSV files from C6

from datetime import datetime
import pandas as pd


def extract_file_data(tmp_file_name, file_date):
    df = pd.read_csv(f"data/tmp_files/{tmp_file_name}", sep=';')
    data = df.to_dict(orient='records')
    file_data = {
        "file_date" : file_date,
        "data" : data
    }
    return file_data


def extract_date(tmp_file_name):
    try:
        date = tmp_file_name.split('_')[1].split('.csv')[0]
        date_object = datetime.strptime(date, '%Y-%m-%d')
        month = date_object.strftime('%m')
        year = date_object.year
        return f'{year}-{month}'
    except Exception as e:
        print(f'[ERROR] Failed extracting date: {e}')
        return None
