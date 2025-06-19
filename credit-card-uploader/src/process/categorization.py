import re
from difflib import SequenceMatcher
import process.ai.ai as ai
import db.db_client as db_client


def categorize_transaction(counter, transaction_description, transaction_amount, transaction_date, categories_dict, use_ai):
    description = _clean_description(transaction_description)
    category = ""

    for keyword, label in categories_dict.items():
        # Keyword contains description
        if keyword.lower() in description:
            category = label
            break
        
        # All words (tokens) of keyword are in description
        if all(word in description for word in keyword.lower().split()):
            category = label
            break
        
        # String similarity
        highest_similarity = 0.0
        similarity = _string_similarity(keyword, description)
        if similarity > highest_similarity and similarity > 0.7:
                highest_similarity = similarity
                category = label

    if category != "":
         print(f" - Transaction #{counter} '{description}' - Matched as pre-saved category: {category}")
    else:
         if use_ai:
            category = ai.ai_categorize_transaction(description, transaction_amount, transaction_date)
            db_client.db_append_ai_category(category, description)
            categories_dict[description] = category 
            print(f" - Transaction #{counter} '{description}' - Categorized with AI as: {category}")

    return category


def _clean_description(desc: str) -> str:
    desc = re.sub(r"\s+", " ", desc).strip()
    return re.sub(r'[^a-zA-ZÀ-ú\s]', '', desc).strip().lower()

def _string_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()
