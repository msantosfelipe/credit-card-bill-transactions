import db_helper
import process_tag_c6
import db_helper

def process_tag_from_import(bank_name, collection, tagsCollection, file_date):
    print(f'[INFO] Starting tag process')

    if bank_name == db_helper.mongo_collection_c6:
        query = {'file_date': file_date}
        bill = collection.find_one(query)
        process_tag_c6.process_tag(bill, collection, tagsCollection, False)
    else:
        print(f'[ERROR] Invalid bank_name: {bank_name}')
        return None

def getTags(dbCLient):
    tagsCollection = dbCLient[db_helper.mongo_collection_tags]
    tags_data = tagsCollection.find({}, {"_id": 0})
    tags_dict = {}

    for tag_data in tags_data:
        name = tag_data["name"]
        keywords = tag_data["keywords"]
        tags_dict[name] = keywords
    
    return tags_dict

if __name__ == '__main__':
    doManual = input('Do manual processment? (Y/n) ')
    dbCLient = db_helper.getDbClient()
    collection = dbCLient[db_helper.mongo_collection_c6]
    all_documents = collection.find()
    for document in all_documents:
        process_tag_c6.process_tag(document, collection, getTags(dbCLient), doManual)    
