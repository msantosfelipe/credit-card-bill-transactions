from db.db_client import db_find_tags


def process_tag(file_data, fields_map):
    tags_dict = db_find_tags()
    transactions = file_data['data']

    counter = 0
    for transaction in transactions:
        counter+=1
        
        if transaction.get('tag', '') != '':
            continue
        customProcessment(counter, transaction, tags_dict, fields_map)
    print('[INFO] All tags updated!')


def customProcessment(counter, transaction, tags_dict, fields_map):
    for label, tags in tags_dict.items():
        tagTransaction(counter, transaction, label, tags, fields_map)


def tagTransaction(counter, transaction, label, tags, fields_map):

    description = transaction[fields_map["description_field_label"]]
    value = transaction[fields_map["value_field_label"]]
    if any(substring in description for substring in tags):
        transaction['tag'] = label
        print(f'Transaction #{counter} tagged with {label} - {description} / R${value}')
