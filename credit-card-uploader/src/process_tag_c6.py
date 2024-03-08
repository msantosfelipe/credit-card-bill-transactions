import tags

def process_tag(bill, collection, doManual):
    transactions = bill['data']

    counter = 0
    totalTransactions = len(transactions)
    
    for transaction in transactions:
        counter+=1
        if transaction.get('tag', '') != '':
            continue

        customProcessment(counter, transaction)
        
        if doManual == 'Y' or doManual == 'y':
            manualProcessment(counter, transaction, totalTransactions)

    updateCollection(transactions, collection, bill['_id'])
    print('[INFO] All tags updated!')

def customProcessment(counter, transaction):
    tagTransaction(counter, transaction, tags.tagUber.items())
    tagTransaction(counter, transaction, tags.tag99.items())
    tagTransaction(counter, transaction, tags.tagIfood.items())
    tagTransaction(counter, transaction, tags.tagSubscriptions.items())
    tagTransaction(counter, transaction, tags.tagMarket.items())

def tagTransaction(counter, transaction, tags):
    description = transaction['Descrição']
    value = transaction['Valor (em R$)']
    for label, substrings in tags:
        if any(substring in description for substring in substrings):
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