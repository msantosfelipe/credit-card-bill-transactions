import os
import pandas as pd
import process.ai.openai as ai
import process.ai.qdrant as qdrant
from datetime import datetime
import db.db_client as db_client


def validate_processed_file(bank_name, tmp_file_name):
    return db_client.db_find_uploaded_data_by_name_and_bank(bank_name, tmp_file_name)


def process_file(tmp_file_name, bank_name, categories_dict):
    if bank_name == "c6":
        file_date = _extract_date_c6(tmp_file_name)
        file_data = _extract_file_data(tmp_file_name, file_date)
        bill = _build_payload_c6(file_data, categories_dict)
    elif bank_name == "xp":
        file_date = _extract_date_xp(tmp_file_name)
        file_data = _extract_file_data(tmp_file_name, file_date)
        bill = _build_payload_xp(file_data, categories_dict)
    else:
        print(f'[ERROR] Invalid bank_name: {bank_name}')
    
    if file_data == None:
        return False
    
    db_client.db_file_data_insert(bank_name, tmp_file_name, file_date, file_data, bill)
    return True


def delete_file(tmp_file_name):
    os.remove(f"data/tmp_files/{tmp_file_name}")


def refresh_bills_categories(bills, use_ai):
    categories_dict = reverse_categories(db_client.db_find_categories())
    if use_ai:
        qdrant.update_qdrant_collection(categories_dict)
    return
    for bill in bills:
        file_date = bill["file_date"]
        bank = bill["bank"]
        print(f"[INFO] Refreshing categories of bill {file_date} from {bank}")
        for i, transaction in enumerate(bill["data"]):
            transaction["category"] = ""
            description = transaction["description"]
            amount = transaction["amount"]
            purchase_date = transaction["purchase_date"]

            matched = False
            for substring, label in categories_dict.items():
                if substring.lower() in description.lower():
                    transaction["category"] = label
                    print(f' - Transaction #{i+1} categorized with {label} - {description} / R${amount}')
                    matched = True
                    break
            if use_ai and not matched:
                category = ai.categorize_transaction(description, amount, purchase_date)
                transaction["category"] = category
                db_client.db_append_ai_category(category, description)
                categories_dict[description] = category
        
        db_client.db_update_bill(file_date, bank, bill["data"])
    

def _extract_file_data(tmp_file_name, file_date):
    df = pd.read_csv(f"data/tmp_files/{tmp_file_name}", sep=';')
    data = df.to_dict(orient='records')
    file_data = {
        "file_date" : file_date,
        "data" : data
    }
    return file_data


def _category_processment(counter, transaction, categories_dict, fields_map):
    for substring, label in categories_dict.items():
        description = transaction[fields_map["description_field_label"]]
        value = transaction[fields_map["value_field_label"]]
        if substring.lower() in description.lower():
            print(f'   - Transaction #{counter} categorized with {label} - {description} / R${value}')
            return label
    return ""


def _get_category_fields_map(bank):
    if bank == "c6":
        return {"description_field_label": "Descrição", "value_field_label" : "Valor (em R$)"}
    else:
        return {"description_field_label": "Estabelecimento", "value_field_label" : "Valor"}


# Converts this: {"FOOD": ["mcdonalds", "bk"], "APP": ["99APP", "uber"]}
# Into this: {"mcdonalds": "FOOD", "bk": "FOOD", "99APP": "APP", "uber": "APP"}
def reverse_categories(categories_dict):
    substring_to_label = {}
    for label, substrings in categories_dict.items():
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


def _build_payload_c6(file_data, categories_dict):
    data = []
    for i, transaction in enumerate(file_data["data"]):
        data.append({
            "purchase_date" : transaction["Data de Compra"],
            "card_holder": transaction["Nome no Cartão"],
            "card_digits": transaction["Final do Cartão"],
            "description": transaction["Descrição"],
            "amount": transaction["Valor (em R$)"],
            "installment": transaction["Parcela"] if (transaction["Parcela"] != "Única") else "-",
            "category": _category_processment(i+1, transaction, categories_dict, _get_category_fields_map("c6")),
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


def _build_payload_xp(file_data, categories_dict):
    data = []
    for i, transaction in enumerate(file_data["data"]):
        data.append({
            "purchase_date" : transaction["Data"],
            "card_holder": transaction["Portador"],
            "card_digits": "",
            "description": transaction["Estabelecimento"],
            "amount": transaction["Valor"],
            "installment": str(transaction["Parcela"]).replace(" de ", "/"),
            "category": _category_processment(i+1, transaction, categories_dict, _get_category_fields_map("xp")),
        })
    return {
        "file_date" : file_data["file_date"],
        "bank" : "xp",
        "data" : data,
    }
