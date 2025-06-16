from openai import OpenAI
import json
import os

client = None
CATEGORIES_AI_FILE_PATH = os.environ.get("CATEGORIES_AI_FILE_PATH")
ai_model = os.environ.get("OPEN_API_MODEL")

def init_ai_client():
    global client 
    client = OpenAI()

def categorize_transaction(description, value, date):
    print(f"   - Categorizing transaction using AI model: {ai_model}")
    prompt = (
        f"You are an assistent that categorizes credit card transactions in categories as "
        f"Transport, Food, Trip, Market, Drugstore, Entertainament etc. "
        f"Description: {description}; "
        f"Value: {value}; "
        f"Date: {date}; "
        f"What is the most appropriate category for this transaction? "
        f"Answer directly only with the category name, no explanations"
    )

    completion = client.chat.completions.create(
        model=ai_model,
        messages=[
            {
                "role": "user", 
                "content": prompt,
            }
        ]
    )
    category = completion.choices[0].message.content

    categories = get_ai_categories_from_file()
    existing = next((item for item in categories if item["name"] == category), None)
    if existing:
        if description not in existing["keywords"]:
            existing["keywords"].append(description)
    else:
        categories.append({
            "name": category,
            "keywords": [description]
        })
    
    with open(CATEGORIES_AI_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=4, ensure_ascii=False)

    print(f"      - Description: {description} - AI response: {completion.choices[0].message.content}")
    return ""
    
def get_ai_categories_from_file():
    if os.path.exists(CATEGORIES_AI_FILE_PATH):
        with open(CATEGORIES_AI_FILE_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []