# scripts/save_categories_single.py

import sys
import os
import time
import json
import requests
import psycopg2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings

class CategoryFetcherSingle:
    def __init__(self, access_token):
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.allegro.public.v1+json"
        }

    def fetch_category_children(self, parent_id=None):
        url = f"{settings.api_url}/sale/categories"
        if parent_id:
            url += f"?parent.id={parent_id}"

        retries = 0
        while retries < 3:
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 429:
                    print("⏳ Too Many Requests! Czekam 60 sekund...")
                    time.sleep(60)
                    continue
                response.raise_for_status()
                return response.json()["categories"]
            except requests.exceptions.RequestException as e:
                retries += 1
                print(f"❌ Błąd pobierania kategorii dla parent_id={parent_id} (próba {retries}/3): {e}")
                time.sleep(5)
        print(f"❌❌ Nie udało się pobrać kategorii parent_id={parent_id} po 3 próbach. Pomijam.")
        return []

class CategorySaverSingle:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="allegro_project",
            user="postgres",
            password="Advox24",
            host="localhost",
            port="5433"
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.existing_ids = self._load_existing_ids()
        self.saved_counter = 0

    def _load_existing_ids(self):
        self.cur.execute("SELECT id FROM allegro_category")
        return set(row[0] for row in self.cur.fetchall())

    def save_category(self, cat):
        cat_id = cat["id"]
        if cat_id in self.existing_ids:
            return False

        name = cat["name"]
        parent = cat.get("parent")
        parent_id = parent.get("id") if isinstance(parent, dict) else None
        leaf = cat["leaf"]

        self.cur.execute("""
            INSERT INTO allegro_category (id, name, parent_id, leaf)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (cat_id, name, parent_id, leaf))

        self.existing_ids.add(cat_id)
        self.saved_counter += 1

        return True

    def close(self):
        self.cur.close()
        self.conn.close()

# =======================
# START
# =======================

def main():
    # Wczytaj token
    with open("token.json", "r") as f:
        token_data = json.load(f)
    access_token = token_data["access_token"]

    fetcher = CategoryFetcherSingle(access_token)
    saver = CategorySaverSingle()

    queue = [None]  # Start od korzenia
    total_processed = 0

    print("\u23f3 Rozpoczynam pobieranie i zapisywanie kategorii Allegro pojedynczo...")

    while queue:
        parent_id = queue.pop(0)
        children = fetcher.fetch_category_children(parent_id)

        print(f"⏩ Przetwarzam kategorię nadrzędną: {parent_id if parent_id else 'ROOT'}, znaleziono {len(children)} dzieci.")

        for child in children:
            total_processed += 1
            print(f"➡️  [{total_processed}] Pobieram kategorię ID={child['id']} - '{child['name']}'")
            saved = saver.save_category(child)
            if saved:
                print(f"✅ Zapisano kategorię ID={child['id']}")
            else:
                print(f"ℹ️ Kategoria ID={child['id']} już istnieje w bazie.")
            queue.append(child["id"])  # Dodajemy dzieci do kolejki

        time.sleep(0.1)  # Szybkie pobieranie, ale z szansą na 429

    print(f"\n✅ Proces zakończony.")
    print(f"➡️ Nowych kategorii zapisanych: {saver.saved_counter}")
    print(f"➡️ Łącznie kategorii przetworzonych: {total_processed}")
    saver.close()

if __name__ == "__main__":
    main()