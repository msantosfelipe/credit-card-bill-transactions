from db.db_client import db_find_tags


def process_tag(file_data):
    tags_dict = db_find_tags()
    transactions = file_data['data']

    counter = 0
    for transaction in transactions:
        counter+=1
        
        if transaction.get('tag', '') != '':
            continue
        customProcessment(counter, transaction, tags_dict)
    print('[INFO] All tags updated!')


def customProcessment(counter, transaction, tags_dict):
    for label, tags in tags_dict.items():
        tagTransaction(counter, transaction, label, tags)


def tagTransaction(counter, transaction, label, tags):
    description = transaction['Descrição']
    value = transaction['Valor (em R$)']
    if any(substring in description for substring in tags):
        transaction['tag'] = label
        print(f'Transaction #{counter} tagged with {label} - {description} / R${value}')
