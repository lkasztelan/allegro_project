# scripts/export_leaf_groups_json_and_txt.py

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

# Mapa: parent_id → lista dzieci [{id, name}]
leaf_by_parent = defaultdict(list)

for cat_id, cat in categories.items():
    if cat["leaf"] and cat["parent_id"]:
        leaf_by_parent[cat["parent_id"]].append({
            "id": cat_id,
            "name": cat["name"]
        })

# Przygotuj dane do zapisania
json_data = []
txt_lines = []

for parent_id, children in leaf_by_parent.items():
    path = build_path(parent_id)
    key_path = "\\".join(path) + "\\"

    # JSON: pełna struktura
    json_data.append({
        "id": parent_id,
        "path": key_path,
        "children": children  # każde dziecko ma {id, name}
    })

    # TXT: ścieżka + ID
    txt_lines.append(f"{key_path} [ID: {parent_id}]")
    for child in sorted(children, key=lambda x: x["name"]):
        txt_lines.append(f"- {child['name']} [ID: {child['id']}]")
    txt_lines.append("")  # pusty wiersz między grupami

# Zapis JSON
with open("leaf_groups.json", "w", encoding="utf-8") as f_json:
    json.dump(json_data, f_json, ensure_ascii=False, indent=2)

# Zapis TXT
with open("leaf_groups.txt", "w", encoding="utf-8") as f_txt:
    f_txt.write("\n".join(txt_lines))

print(f"✅ Zapisano leaf_groups.json ({len(json_data)} grup) i leaf_groups.txt ({len(txt_lines)} linii).")

cur.close()
conn.close()
