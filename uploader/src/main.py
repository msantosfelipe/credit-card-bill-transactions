from storage.firebase_storage_client import list_pending_files_to_process, download_file

# 1- List all files in the storage - ok
# 2- Look in DB if is not processed
# 3- Download pending files - ok
# 4- Process the file
# 5- Delete the file
def process_from_storage():
    all_files = list_pending_files_to_process()
    for file in all_files:
        # TODO check in DB
        download_file(file, file.split("/")[-1])

if __name__ == '__main__':
    process_from_storage()
