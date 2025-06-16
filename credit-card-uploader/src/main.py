import db.db_client as db_client
import sys
import process.process as process
import process.categories_control as categories_control
from process.ai import init_ai_client
from storage.firebase_storage_client import list_files_from_storage, download_file


def _process_from_storage():
    all_files = list_files_from_storage()
    categories_dict = process.reverse_categories(db_client.db_find_categories())
    num_files = len(all_files)
    for i, file in enumerate(all_files):
        print(f"[INFO] Processing file {i+1} of {num_files}")
        tmp_file_name = file.split("/")[-1]
        bank_name = file.split("/")[1]
        
        if process.validate_processed_file(bank_name, tmp_file_name):
            print(f'[WARN] File already imported: {tmp_file_name} from bank {bank_name}')
            continue

        download_file(file, tmp_file_name)
        processed = process.process_file(tmp_file_name, bank_name, categories_dict)
        if processed:
            process.delete_file(tmp_file_name)
            print(f"[INFO] File: {file} processed and deleted")
        else:
            print(f"[ERROR] There was a problema processing file {file} and it will not be deleted")


if __name__ == '__main__':
    arguments = sys.argv[1:]
    if arguments and arguments[0] == "refresh":
        use_ai = len(arguments) > 1 and arguments[1] == "ai"
        init_ai_client()
        print(f'\n*** Starting Refreshing with categories script. Use AI: {use_ai} ***\n')
        categories_control.upload_categories()
        bills = db_client.db_find_all_bills()
        process.refresh_bills_categories(bills, use_ai)

        print("[INFO] All bills were refreshed!")
        exit(0)

    print('\n*** Starting import script ***\n')
    if arguments and arguments[0] == "clean":
        print('[WARN] Dropping all collections!')
        db_client.db_drop_all_collections()
    
    categories_control.upload_categories()
    _process_from_storage()
