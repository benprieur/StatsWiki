import sqlite3
from constants import DB_NAME, SUPPORTED_LANGUAGES, SUPPORTED_YEARS

langs = SUPPORTED_LANGUAGES
years = SUPPORTED_YEARS

def create_or_update_views():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for lang in langs:

        view_name = f"{lang}_view"
        cursor.execute(f"DROP VIEW IF EXISTS {view_name}")
        conn.commit()

        view_query_parts = []
        for year in years:
            table_name = f"{lang}_{year}"
            view_query_parts.append(f"SELECT article, views FROM {table_name}")

        view_query = f"CREATE VIEW {view_name} AS " + " UNION ALL ".join(view_query_parts) + ";"
        print(view_query)
        try:
            cursor.execute(view_query)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de la vue {view_name}: {e}")

    conn.close()

def create_or_update_view_en():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    lang = 'en'
            
    view_name = f"{lang}_view"
    cursor.execute(f"DROP VIEW IF EXISTS {view_name}")
    conn.commit()

    view_query_parts = []
    for year in years:
        table_name = f"{lang}_{year}"
        view_query_parts.append(f"SELECT article, views FROM {table_name}")

    view_query = f"CREATE VIEW {view_name} AS " + " UNION ALL ".join(view_query_parts) + ";"
    print(view_query)

    try:
        cursor.execute(view_query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la vue {view_name}: {e}")

    conn.close()

