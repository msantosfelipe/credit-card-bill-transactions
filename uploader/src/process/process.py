import os
from process.process_c6 import extract_file_data as process_c6
from process.process_c6 import extract_date as extract_date_c6
from db.db_client import db_find_uploaded_data_by_name, db_file_data_insert


def validate_processed_file(bank_name, tmp_file_name):
    return db_find_uploaded_data_by_name(bank_name, tmp_file_name)


def process_file(tmp_file_name, bank_name):
    print(f"[INFO] Processing file: {tmp_file_name} from bank {bank_name}")

    if bank_name == "c6":
        file_date = extract_date_c6(tmp_file_name)
        file_data = process_c6(tmp_file_name, file_date)
    else:
        print(f'[ERROR] Invalid bank_name: {bank_name}')
        return False
    
    if file_data == None:
        return False

    db_file_data_insert(bank_name, tmp_file_name, file_date, file_data)
    return True


def delete_file(tmp_file_name):
    os.remove(f"data/tmp_files/{tmp_file_name}")
