import os
import pandas as pd
import process.ai as ai
from datetime import datetime
import db.db_client as db_client


def validate_processed_file(bank_name, tmp_file_name):
    return db_client.db_find_uploaded_data_by_name_and_bank(bank_name, tmp_file_name)


def process_file(tmp_file_name, bank_name, tags_dict):
    if bank_name == "c6":
        file_date = _extract_date_c6(tmp_file_name)
        file_data = _extract_file_data(tmp_file_name, file_date)
        bill = _build_payload_c6(file_data, tags_dict)
    elif bank_name == "xp":
        file_date = _extract_date_xp(tmp_file_name)
        file_data = _extract_file_data(tmp_file_name, file_date)
        bill = _build_payload_xp(file_data, tags_dict)
    else:
        print(f'[ERROR] Invalid bank_name: {bank_name}')
    
    if file_data == None:
        return False
    
    db_client.db_file_data_insert(bank_name, tmp_file_name, file_date, file_data, bill)
    return True


def delete_file(tmp_file_name):
    os.remove(f"data/tmp_files/{tmp_file_name}")


def refresh_bills_tags(bills, use_ai):
    tags_dict = reverse_tags(db_client.db_find_tags())
    for bill in bills:
        file_date = bill["file_date"]
        bank = bill["bank"]
        print(f"[INFO] Refreshing tags of bill {file_date} from {bank}")
        for i, transaction in enumerate(bill["data"]):
            transaction["tag"] = ""
            description = transaction["description"]
            amount = transaction["amount"]
            purchase_date = transaction["purchase_date"]

            matched = False
            for substring, label in tags_dict.items():
                if substring.lower() in description.lower():
                    transaction["tag"] = label
                    print(f'   - Transaction #{i+1} tagged with {label} - {transaction["description"]} / R${amount}')
                    matched = True
                    break
            if use_ai and matched:
                transaction["tag"] = ai.categorize_transaction(description, amount, purchase_date)
        
        db_client.db_update_bill(file_date, bank, bill["data"])


def _extract_file_data(tmp_file_name, file_date):
    df = pd.read_csv(f"data/tmp_files/{tmp_file_name}", sep=';')
    data = df.to_dict(orient='records')
    file_data = {
        "file_date" : file_date,
        "data" : data
    }
    return file_data


def _tag_processment(counter, transaction, tags_dict, fields_map):
    for substring, label in tags_dict.items():
        description = transaction[fields_map["description_field_label"]]
        value = transaction[fields_map["value_field_label"]]
        if substring.lower() in description.lower():
            print(f'   - Transaction #{counter} tagged with {label} - {description} / R${value}')
            return label
    return ""


def _get_tag_fields_map(bank):
    if bank == "c6":
        return {"description_field_label": "Descrição", "value_field_label" : "Valor (em R$)"}
    else:
        return {"description_field_label": "Estabelecimento", "value_field_label" : "Valor"}


# Converts this: {"FOOD": ["mcdonalds", "bk"], "APP": ["99APP", "uber"]}
# Into this: {"mcdonalds": "FOOD", "bk": "FOOD", "99APP": "APP", "uber": "APP"}
def reverse_tags(tags_dict):
    substring_to_label = {}
    for label, substrings in tags_dict.items():
        for substring in substrings:
            substring_to_label[substring.lower()] = label
    return substring_to_label


# C6 functions

def _extract_date_c6(tmp_file_name):
    try:
        date = tmp_file_name.split('_')[1].split('.csv')[0]
        date_object = datetime.strptime(date, '%Y-%m-%d')
        month = date_object.strftime('%m')
        year = date_object.year
        return f'{year}-{month}'
    except Exception as e:
        print(f'[ERROR] Failed extracting date: {e}')
        return None


def _build_payload_c6(file_data, tags_dict):
    data = []
    for i, transaction in enumerate(file_data["data"]):
        data.append({
            "purchase_date" : transaction["Data de Compra"],
            "card_holder": transaction["Nome no Cartão"],
            "card_digits": transaction["Final do Cartão"],
            "description": transaction["Descrição"],
            "amount": transaction["Valor (em R$)"],
            "installment": transaction["Parcela"] if (transaction["Parcela"] != "Única") else "-",
            "tag": _tag_processment(i+1, transaction, tags_dict, _get_tag_fields_map("c6")),
        })
    return {
        "file_date" : file_data["file_date"],
        "bank" : "c6",
        "data" : data,
    }


# XP functions

def _extract_date_xp(tmp_file_name):
    try:
        date = tmp_file_name.split('Fatura')[1].split('.csv')[0]
        date_object = datetime.strptime(date, '%Y-%m-%d')
        month = date_object.strftime('%m')
        year = date_object.year
        return f'{year}-{month}'
    except Exception as e:
        print(f'[ERROR] Failed extracting date: {e}')
        return None


def _build_payload_xp(file_data, tags_dict):
    data = []
    for i, transaction in enumerate(file_data["data"]):
        data.append({
            "purchase_date" : transaction["Data"],
            "card_holder": transaction["Portador"],
            "card_digits": "",
            "description": transaction["Estabelecimento"],
            "amount": transaction["Valor"],
            "installment": str(transaction["Parcela"]).replace(" de ", "/"),
            "tag": _tag_processment(i+1, transaction, tags_dict, _get_tag_fields_map("xp")),
        })
    return {
        "file_date" : file_data["file_date"],
        "bank" : "xp",
        "data" : data,
    }
