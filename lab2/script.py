import csv
import json
import requests
import os
from dotenv import load_dotenv   

load_dotenv()                   

API_KEY = os.getenv("GITHUB_TOKEN")
if not API_KEY:
    raise Exception("Не найден GITHUB_TOKEN в .env файле")

BASE_URL = "https://models.inference.ai.azure.com"
MODEL_NAME = "gpt-4o-mini"  

INPUT_CSV = "reviews.csv"
OUTPUT_JSON = "result.json"

def ask_llm(text):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Классифицируй тональность и тему. Пиши тему на английском с маленькой буквы. Верни JSON: {\"sentiment\":\"positive/negative/neutral\", \"topic\":\"...\"}"},
            {"role": "user", "content": text}
        ],
        "response_format": {"type": "json_object"}
    }
    resp = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API error {resp.status_code}: {resp.text}")

reviews = []
with open(INPUT_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        reviews.append(row["review_text"])

results = []
for idx, rev in enumerate(reviews, 1):
    print(f"Обработка {idx}/{len(reviews)}")
    try:
        answer = ask_llm(rev)
        results.append({"id": idx, "review": rev, "llm_answer": json.loads(answer)})
    except Exception as e:
        print(f"Ошибка: {e}")
        results.append({"id": idx, "review": rev, "error": str(e)})

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Готово! Результат в {OUTPUT_JSON}")