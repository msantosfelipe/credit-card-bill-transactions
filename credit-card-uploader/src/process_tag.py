import db_helper
import process_tag_c6

c6 = 'c6'

def process_tag_from_import(bank_name, collection, file_date):
    print(f'[INFO] Starting tag process')

    if bank_name == c6:
        query = {'file_date': file_date}
        bill = collection.find_one(query)
        process_tag_c6.process_tag(bill, collection, False)
    else:
        print(f'[ERROR] Invalid bank_name: {bank_name}')
        return None

if __name__ == '__main__':
    doManual = input('Do manual processment? (Y/n) ')
    collection = db_helper.getCollection(c6)
    all_documents = collection.find()
    for document in all_documents:
        process_tag_c6.process_tag(document, collection, doManual)    
