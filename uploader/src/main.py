from storage.firebase_storage_client import list_pending_files_to_process, download_file
from process.process import validate_processed_file, process_file, delete_file
from process.tags import process_tags


def process_from_storage():
    all_files = list_pending_files_to_process()

    for file in all_files:
        print(f'**************************************')

        tmp_file_name = file.split("/")[-1]
        bank_name = file.split("/")[1]
        
        if validate_processed_file(bank_name, tmp_file_name):
            print(f'[WARN] File from bank_name {bank_name} and name {tmp_file_name} already exists')
            continue

        download_file(file, tmp_file_name)
        result_ok = process_file(tmp_file_name, bank_name)
        if (result_ok):
            delete_file(tmp_file_name)
            print(f"[INFO] File: {file} processed and deleted.")
        else:
            print(f"[ERROR] There was a problema processing file {file} and it will not be deleted")


if __name__ == '__main__':
    process_tags()
    process_from_storage()
