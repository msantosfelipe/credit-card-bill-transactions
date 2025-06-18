from openai import OpenAI
import json, os
from datetime import datetime


CATEGORIES_AI_FILE_PATH = os.environ.get("CATEGORIES_AI_FILE_PATH")
VALID_CATEGORIES = ["Transport, Food, Market, Drugstore, Entertainment, Education, Healthcare, Other"]


def categorize_transaction(transaction_description, value, date):
    ai_model = os.environ.get("OPEN_API_MODEL")
    print(f"  - Categorizing transaction using AI model: {ai_model}")
    prompt = _build_prompt(transaction_description, value, date)

    completion = client.chat.completions.create(
        model=ai_model,
        messages=[
            {
                "role": "user", 
                "content": prompt,
            }
        ],
    )

    category = completion.choices[0].message.content
    print(f"   - Description: {transaction_description} - AI response: {category}")
    
    normalized_category = category.split(" ")[0]
    _update_dict_file(normalized_category, transaction_description)
    return normalized_category


def _build_prompt(description: str, value: float, date: str) -> str:
    examples = """
        **Categorizations examples:**
        1. Description: "IFOOD *LANCHE"; Value: 45.50; Date: 10/03/2023 → Food
        3. Description: "DROGARIA SAUDE"; Value: 32.00; Date: 11/03/2023 → Drugstore
        4. Description: "Udemy"; Value: 39.90; Date: 01/03/2023 → Education
        5. Description: "Bar Cerveja"; Value: 39.90; Date: 01/03/2023 → Entertainment
        6. Description: "FITNESS"; Value: 39.90; Date: 01/03/2023 → Healthcare
    """

    prompt = f"""
        You are an assistent that categorizes credit card transactions ONLY in these categories: {', '.join(VALID_CATEGORIES)}.

        {examples}

        Description: {description};
        Value: {value};
        Date: {date} - {_get_weekday(date)};
        
        Transactions descriptions are in PT-BR.
        What is the most appropriate category for this transaction?
        Answer DIRECTLY in one world, ONLY with the category name, no explanations
    """

    return prompt


def _get_weekday(date_str: str) -> str:
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    return date_obj.strftime("%A")


def _update_dict_file(category, transaction_description):
    categories = _get_ai_categories_from_file()
    existing = next((item for item in categories if item["name"] == category), None)
    if existing:
        if transaction_description not in existing["keywords"]:
            existing["keywords"].append(transaction_description)
    else:
        categories.append({
            "name": category,
            "keywords": [transaction_description]
        })
    
    with open(CATEGORIES_AI_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=4, ensure_ascii=False)


def _get_ai_categories_from_file():
    if os.path.exists(CATEGORIES_AI_FILE_PATH):
        with open(CATEGORIES_AI_FILE_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []


def _init_client():
    return OpenAI()


client = _init_client()