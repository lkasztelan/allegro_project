# scripts/save_categories_to_db.py

import sys
import os
import time
import json
import requests
import psycopg2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings

# 1. Wczytanie tokena
with open("token.json", "r") as f:
    token_data = json.load(f)
access_token = token_data["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/vnd.allegro.public.v1+json"
}

# 2. Połączenie z bazą
conn = psycopg2.connect(
    dbname="allegro_project",
    user="postgres",
    password="Advox24",
    host="localhost",
    port="5433"
)
conn.autocommit = True
cur = conn.cursor()

# 3. Pobranie ID już zapisanych kategorii
cur.execute("SELECT id FROM allegro_category")
existing_ids = set(row[0] for row in cur.fetchall())
print(f"🧠 Wczytano {len(existing_ids)} istniejących kategorii z bazy.")

# 4. Funkcja zapisująca kategorię
counter = 0
def save_category(cat):
    global counter
    cat_id = cat["id"]
    if cat_id in existing_ids:
        return  # pomijamy już istniejącą kategorię

    name = cat["name"]
    parent = cat.get("parent")
    parent_id = parent.get("id") if isinstance(parent, dict) else None
    leaf = cat["leaf"]

    cur.execute("""
        INSERT INTO allegro_category (id, name, parent_id, leaf)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (cat_id, name, parent_id, leaf))

    existing_ids.add(cat_id)
    counter += 1
    if counter % 100 == 0:
        print(f"📦 Zapisano nowych: {counter}")

# 5. Funkcja pobierająca i zapisująca drzewo kategorii
def fetch_all_categories():
    queue = [None]  # start od korzenia

    while queue:
        parent_id = queue.pop(0)

        # Pomijamy, jeśli już w bazie są dzieci tej kategorii
        if parent_id in existing_ids:
            continue

        url = f"{settings.api_url}/sale/categories"
        if parent_id:
            url += f"?parent.id={parent_id}"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            print(f"⏱️ TIMEOUT przy pobieraniu: {url}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"❌ Błąd pobierania: {e}")
            continue

        categories = response.json()["categories"]

        for cat in categories:
            save_category(cat)
            queue.append(cat["id"])

        time.sleep(0.3)  # 💤 delikatne opóźnienie

# 6. Start
print("⏳ Rozpoczynam uzupełnianie kategorii...")
fetch_all_categories()
print(f"✅ Zakończono. Zapisano {counter} nowych kategorii.")

cur.close()
conn.close()
