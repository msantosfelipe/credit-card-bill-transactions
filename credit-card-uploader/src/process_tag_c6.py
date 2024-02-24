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
    tagIfood(counter, transaction)
    tag99(counter, transaction)
    tagSubscriptions(counter, transaction)

def tagIfood(counter, transaction):
    label = 'Ifood'
    description = transaction['Descrição']
    value = transaction['Valor (em R$)']
    if 'IFOOD' in description:
        transaction['tag'] = label
        print(f'Transaction #{counter} tagged with {label} - {description} / R${value}')

def tag99(counter, transaction):
    label = '99'
    substrings = ['99APP', '99*']
    description = transaction['Descrição']
    value = transaction['Valor (em R$)']
    if any(substring in description for substring in substrings):
        transaction['tag'] = label
        print(f'Transaction #{counter} tagged with {label} - {description} / R${value}')

def tagSubscriptions(counter, transaction):
    label = 'Subscription'
    substrings = ['ALPHA FITNESS', 'SOCIO ESQUAD', 'NETFLIX', 'DGOSKY', 'LIVELO', 'SPOTIFY', 'GOOGLE YOUTUBE MEMBER', 'SERASA', 'PRODUTOS GLOBO']
    description = transaction['Descrição']
    value = transaction['Valor (em R$)']
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