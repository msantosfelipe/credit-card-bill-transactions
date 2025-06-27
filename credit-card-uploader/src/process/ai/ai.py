from openai import OpenAI
import json, os
from datetime import datetime


CATEGORIES_AI_FILE_PATH = os.environ.get("CATEGORIES_AI_FILE_PATH")
VALID_CATEGORIES = [
    "Transport", 
    "Food", 
    "Market", 
    "Drugstore", 
    "Entertainment", 
    "Education", 
    "Healthcare", 
    "Other",
]


def ai_categorize_transaction(transaction_description, value, date):
    print(f" - Categorizing '{transaction_description}' with AI...")
    ai_model = os.environ.get("OPEN_API_MODEL")
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
    normalized_category = _normalize_category(category)

    _update_dict_file(normalized_category, transaction_description)
    return normalized_category


def _build_prompt(description: str, value: float, date: str) -> str:
    examples = """
        **Categorizations examples:**
        1. Description: "ifood lanche comida"; Value: 45.50; Date: 10/03/2023 → Food
        3. Description: "droga farma"; Value: 32.00; Date: 11/03/2023 → Drugstore
        4. Description: "udemy"; Value: 39.90; Date: 01/03/2023 → Education
        5. Description: "bar bebida deposito whisky festa ingresso"; Value: 39.90; Date: 01/03/2023 → Entertainment
        6. Description: "fitness academia saude"; Value: 39.90; Date: 01/03/2023 → Healthcare
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


def _normalize_category(category):
    normalized_category = category.strip().split(" ")[0]
    if normalized_category not in VALID_CATEGORIES:
        print(f" - AI category {normalized_category} not in {VALID_CATEGORIES}")
        return "Other"
    return normalized_category

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
