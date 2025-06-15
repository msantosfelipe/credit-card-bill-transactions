import os
import pandas as pd
from datetime import datetime
from db.db_client import db_find_uploaded_data_by_name_and_bank, db_file_data_insert
from process.tags_process import process_tag


def validate_processed_file(bank_name, tmp_file_name):
    return db_find_uploaded_data_by_name_and_bank(bank_name, tmp_file_name)


def process_file(tmp_file_name, bank_name):
    print(f"[INFO] Processing file: {tmp_file_name} from bank {bank_name}")

    if bank_name == "c6":
        file_date = extract_date_c6(tmp_file_name)
        file_data = extract_file_data(tmp_file_name, file_date)
        fields_map = {"description_field_label": "Descrição", "value_field_label" : "Valor (em R$)"}
    elif bank_name == "xp":
        file_date = extract_date_xp(tmp_file_name)
        file_data = extract_file_data(tmp_file_name, file_date)
        fields_map = {"description_field_label": "Estabelecimento", "value_field_label" : "Valor"}
    else:
        print(f'[ERROR] Invalid bank_name: {bank_name}')
    
    if file_data == None:
        return False
    
    process_tag(file_data, fields_map)
    db_file_data_insert(bank_name, tmp_file_name, file_date, file_data)

    return True


def delete_file(tmp_file_name):
    os.remove(f"data/tmp_files/{tmp_file_name}")


def extract_file_data(tmp_file_name, file_date):
    df = pd.read_csv(f"data/tmp_files/{tmp_file_name}", sep=';')
    data = df.to_dict(orient='records')
    file_data = {
        "file_date" : file_date,
        "data" : data
    }
    return file_data


def extract_date_c6(tmp_file_name):
    try:
        date = tmp_file_name.split('_')[1].split('.csv')[0]
        date_object = datetime.strptime(date, '%Y-%m-%d')
        month = date_object.strftime('%m')
        year = date_object.year
        return f'{year}-{month}'
    except Exception as e:
        print(f'[ERROR] Failed extracting date: {e}')
        return None


def extract_date_xp(tmp_file_name):
    try:
        date = tmp_file_name.split('Fatura')[1].split('.csv')[0]
        date_object = datetime.strptime(date, '%Y-%m-%d')
        month = date_object.strftime('%m')
        year = date_object.year
        return f'{year}-{month}'
    except Exception as e:
        print(f'[ERROR] Failed extracting date: {e}')
        return None
