import sys, time
import db.db_client as db_client
import process.process as process
import process.categories_control as categories_control
from storage.firebase_storage_client import list_files_from_storage, download_file
from process.categorization import (
    manual_categorization_counter, ai_categorization_counter
)


def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[{func.__name__}] Duration: {end - start:.2f} seconds")
        return result
    return wrapper


@timing
def _process_from_storage(use_ai):
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
        processed = process.process_file(tmp_file_name, bank_name, categories_dict, use_ai)

        if processed:
            process.delete_file(tmp_file_name)
            print(f"[INFO] File: {file} processed and deleted")
        else:
            print(f"[ERROR] There was a problema processing file {file} and it will not be deleted")


@timing
def _process_refresh(use_ai):
    print(f'\n*** Starting Refreshing with categories script. Use AI: {use_ai} ***\n')
    bills = db_client.db_find_all_bills()
    process.refresh_bills_categories(bills, use_ai)
    if use_ai:
        categories_control.update_hash()

    print("[INFO] All bills were refreshed!")


@timing
def _process_clean():
    print('[WARN] Dropping all collections and removing categories_ai file (if exists)!')
    db_client.db_drop_all_collections()
    categories_control.remove_categories_ai_file()


if __name__ == '__main__':
    arguments = sys.argv[1:]
    use_ai = arguments and "ai" in arguments
    
    if arguments and "clean" in arguments:
        _process_clean()
        exit(0)

    categories_control.upload_categories()

    if arguments and arguments[0] == "refresh":
        _process_refresh(use_ai)
        exit(0)

    print('\n*** Starting import script ***\n')
    _process_from_storage(use_ai)
    print(f"Transactions manually categorized: {manual_categorization_counter}")
    print(f"Transactions categorized with AI: {ai_categorization_counter}")
