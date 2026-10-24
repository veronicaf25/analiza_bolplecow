import os
import sqlite3
import pandas as pd

# Ścieżka do głównego folderu projektu
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, 'data')
CSV_PATH = os.path.join(DATA_DIR, 'dane_pacjenci_bol_plecow.csv')
DB_PATH = os.path.join(DATA_DIR, 'pacjenci.db')

# Upewnij się, że katalog data istnieje
os.makedirs(DATA_DIR, exist_ok=True)

# Automatyczne utworzenie bazy SQLite z pliku CSV, jeśli plik .db jeszcze nie istnieje
if not os.path.exists(DB_PATH) and os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('pacjenci', conn, if_exists='replace', index=False)
    conn.close()