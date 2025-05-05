import os
from dotenv import load_dotenv

# Wczytaj zmienne środowiskowe z pliku .env
load_dotenv()

# Klucz OpenAI ładowany z .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Lista dostępnych Assistantów (Nazwa: ID Assistanta)
ASSISTANTS = {
    "Allegro Kategorie 4.1": "asst_IZ9FLIREx7KRjNufDueY579t",
    "Allegro Kategorie 3o": "asst_MktZkfqzBdWwLDBTNJgGHyA3",
    # Dodaj tutaj kolejne jeśli chcesz
}
