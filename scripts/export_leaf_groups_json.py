# scripts/export_leaf_groups_jsonl.py

import sys
import os
import json
from collections import defaultdict

# Dodaj katalog główny do importów
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import psycopg2

# Połączenie z PostgreSQL
conn = psycopg2.connect(
    dbname="allegro_project",
    user="postgres",
    password="Advox24",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Pobranie kategorii
cur.execute("SELECT id, name, parent_id, leaf FROM allegro_category")
rows = cur.fetchall()

# Mapa kategorii ID -> dane
categories = {
    row[0]: {"name": row[1], "parent_id": row[2], "leaf": row[3]}
    for row in rows
}

# Funkcja do budowania pełnej ścieżki nadrzędnej
def build_path(cat_id):
    path = []
    while cat_id in categories:
        cat = categories[cat_id]
        path.insert(0, cat["name"])
        cat_id = cat["parent_id"]
    return path

# Mapa: parent_id → [leaf_name1, leaf_name2, ...]
leaf_by_parent = defaultdict(list)

for cat_id, cat in categories.items():
    if cat["leaf"] and cat["parent_id"]:
        leaf_by_parent[cat["parent_id"]].append(cat["name"])

# Zapis do pliku JSONL – jedna linia = jedna grupa
with open("leaf_groups.jsonl", "w", encoding="utf-8") as f:
    for parent_id, children in leaf_by_parent.items():
        path = build_path(parent_id)
        key = "\\".join(path) + "\\"
        obj = {key: sorted(children)}
        f.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")

print(f"✅ Zapisano leaf_groups.jsonl z {len(leaf_by_parent)} wierszami (JSON per linia).")

cur.close()
conn.close()
