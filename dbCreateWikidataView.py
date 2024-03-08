import sqlite3
from constants import DB_NAME, SUPPORTED_LANGUAGES

def create_language_views():

    sql_template = """
    CREATE VIEW IF NOT EXISTS {lang}_wikidata_view AS
    SELECT DISTINCT w.qid, 
                    replace(l.article, '''', '&/==+') AS article, 
                    w.en_translation, 
                    w.props
    FROM {lang}_view AS l
    JOIN _wikidata AS w ON replace(replace(w.{lang}_title, ' ', '_'), '''', '&/==+') = replace(l.article, '''', '&/==+');
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for lang in SUPPORTED_LANGUAGES:
        sql_command = sql_template.format(lang=lang)

        try:
            cursor.execute(sql_command)
            print(f"Vue pour la langue '{lang}' créée avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de la vue pour la langue '{lang}': {e}")

    conn.commit()
    conn.close()
create_language_views()
