# db/create_tables.py

# ===== Import systemowych bibliotek do pracy ze ścieżkami
import sys
import os

# ===== Dodaj katalog główny projektu do ścieżki importu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ===== Import pozostałych bibliotek
import psycopg2  # do pracy z PostgreSQL
from config import settings  # teraz będzie działać

# ======================
# 1. Łączymy się z bazą danych PostgreSQL
# ======================
conn = psycopg2.connect(
    dbname="allegro_project",  # możesz też użyć: settings.DB_CONFIG["dbname"]
    user="postgres",
    password="Advox24",
    host="localhost",
    port="5433"
)

# ======================
# 2. Tworzymy kursor (czyli obiekt do wykonywania SQL)
# ======================
cur = conn.cursor()

# ======================
# 3. Tworzymy tabelę z kategoriami
# ======================
create_table_sql = """
CREATE TABLE IF NOT EXISTS allegro_category (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    parent_id VARCHAR,
    leaf BOOLEAN NOT NULL,
    CONSTRAINT fk_parent FOREIGN KEY (parent_id) REFERENCES allegro_category (id) ON DELETE SET NULL
);
"""

# ======================
# 4. Wykonujemy zapytanie
# ======================
cur.execute(create_table_sql)

# ======================
# 5. Zatwierdzamy zmiany i zamykamy połączenie
# ======================
conn.commit()
cur.close()
conn.close()

print("✅ Tabela allegro_category gotowa!")
