# scripts/export_leaf_groups.py

import sys
import os
from collections import defaultdict

# Dodaj katalog główny do importów
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import psycopg2

# Połączenie z bazą danych PostgreSQL
conn = psycopg2.connect(
    dbname="allegro_project",
    user="postgres",
    password="Advox24",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Pobranie wszystkich kategorii
cur.execute("SELECT id, name, parent_id, leaf FROM allegro_category")
rows = cur.fetchall()

# Tworzymy słownik kategorii
categories = {
    row[0]: {
        "id": row[0],
        "name": row[1],
        "parent_id": row[2],
        "leaf": row[3]
    }
    for row in rows
}

# Funkcja budująca pełną ścieżkę kategorii nadrzędnej
def build_path(cat_id):
    path = []
    while cat_id and cat_id in categories:
        cat = categories[cat_id]
        path.insert(0, cat["name"])
        cat_id = cat["parent_id"]
    return path

# Grupujemy leaf-kategorie według ich rodzica
leaf_by_parent = defaultdict(list)

for cat_id, cat in categories.items():
    if cat["leaf"] and cat["parent_id"]:
        leaf_by_parent[cat["parent_id"]].append(cat["name"])

# Zapisujemy wynik do pliku tekstowego
with open("leaf_groups.txt", "w", encoding="utf-8") as f:
    # === Nagłówek wyjaśniający strukturę ===
    f.write("# Plik zawiera końcowe kategorie (leaf = true), pogrupowane według ich rodziców\n")
    f.write("# Format: pełna ścieżka do kategorii nadrzędnej \\ — lista jej podkategorii końcowych\n")
    f.write("# Przykład: RTV\\Telewizory\\ — LED TV, OLED TV\n")
    f.write("# Każda linia = jedna grupa podkategorii leaf\n")
    f.write("\n")

    # Wypisujemy każdą grupę: pełna ścieżka nadrzędna — lista dzieci
    for parent_id, children_names in leaf_by_parent.items():
        path = build_path(parent_id)
        path_str = "\\".join(path) + "\\"  # dodaj końcowy backslash
        children_str = ", ".join(sorted(children_names))
        f.write(f"{path_str} — {children_str}\n")

print(f"✅ Zapisano plik leaf_groups.txt z {len(leaf_by_parent)} grupami kategorii końcowych.")

# Zamykamy połączenie z bazą
cur.close()
conn.close()
