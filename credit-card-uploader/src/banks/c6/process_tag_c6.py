def process_tag(bill, collection, tags_dict, doManual):    
    transactions = bill['data']

    counter = 0
    totalTransactions = len(transactions)
    
    for transaction in transactions:
        counter+=1
        if transaction.get('tag', '') != '':
            continue

        customProcessment(counter, transaction, tags_dict)
        
        if doManual == 'Y' or doManual == 'y':
            manualProcessment(counter, transaction, totalTransactions)

    updateCollection(transactions, collection, bill['_id'])
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

def manualProcessment(counter, transaction, totalTransactions):
    print('-----------------------------------------------------')
    print(f'Transaction {counter} of {totalTransactions}')
    print(transaction)
    tag = input('Enter a new tag for this transaction: ')
    transaction['tag'] = tag
    return

def updateCollection(transactions, collection, id):
    update = {
            '$set': {
                'data': transactions,
            }
        }
    collection.update_one({'_id': id}, update)