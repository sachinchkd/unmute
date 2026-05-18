import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PAGE_ID = os.getenv("FB_PAGE_ID", "balenOfficial")
ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")

url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/posts"

params = {
    "access_token": ACCESS_TOKEN,
    "fields": "id,message,created_time,permalink_url",
    "limit": 100,
}

Path("data").mkdir(exist_ok=True)

with open("data/raw_posts.jsonl", "w", encoding="utf-8") as file:
    while url:
        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            print(data["error"])
            break

        for post in data.get("data", []):
            if "message" in post:
                file.write(json.dumps(post, ensure_ascii=False) + "\n")

        url = data.get("paging", {}).get("next")
        params = {}

print("Done")