import sqlite3
from constants import DB_NAME, SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from datetime import timedelta, date
import calendar

'''
    test_view_fr_2024
'''
import sqlite3
from datetime import date, timedelta
import calendar

def test_view_fr_2024():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    start_date = date(2024, 1, 1)
    number_days_by_year = 366 if calendar.isleap(2024) else 365

    day_columns = [start_date + timedelta(days=i) for i in range(number_days_by_year)]
    day_column_names = [f"D._{day.strftime('%Y%m%d')}" for day in day_columns]
    month_column_names = [f"M._{month:02d}" for month in range(1, 13)]
    
    table_name_day = 'fr_2024_day'
    table_name_month = 'fr_2024_month'
    table_name_year = 'fr_2024'
    table_wikidata = '_wikidata'

    columns_definition_day = ", ".join(day_column_names)
    columns_definition_month = ", ".join(month_column_names)

    sql_command = f"""
            CREATE VIEW test_8 AS
            SELECT
                W.qid,
                W.fr_title,
                W.en_translation,
                W.props,
                {columns_definition_day},
                {columns_definition_month},
                Y.views
            FROM
                _wikidata AS W
                JOIN fr_2024_day AS D ON replace(W.fr_title, ' ', '_') = D.article
                JOIN fr_2024_month AS M ON replace(W.fr_title, ' ', '_') = M.article
                JOIN fr_2024 AS Y ON replace(W.fr_title, ' ', '_') = Y.article;
    """

    try:
        print(sql_command)
        cursor.execute(sql_command)
        #conn.commit()
        
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la vue: {e}")

    conn.close()


'''
    delete_all_views
'''
def delete_all_views():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = "SELECT name FROM sqlite_master WHERE type='view';"
    
    try:
        cursor.execute(query)
        views = cursor.fetchall()
        for view in views:
            cursor.execute(f"DROP VIEW IF EXISTS {view[0]}")
        conn.commit()  
    except Exception as e:
        print(f'Erreur: {e}')
    finally:
        if conn:
            conn.close()



def fix_du_giscard_fix():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for lang in SUPPORTED_LANGUAGES:
        col = f"{lang}_title"
        sql_command = f"""
        SELECT * FROM _wikidata WHERE {col} LIKE '%&/==+%'
        """

        cursor.execute(sql_command)
        rows = cursor.fetchall()

        for row in rows:
            print(row)

    conn.close()  

#test_view_fr_2024()
#query = "PRAGMA table_info('test_view_2');;"


'''
    create_views_alltime
'''
def create_views_alltime():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for lang in SUPPORTED_LANGUAGES:
        view_name = f"{lang}_vue"   
        cols_names = [f"A{year}._{month:02d} AS _{year}{month:02d}" for year in SUPPORTED_YEARS for month in range(1, 13)]
        cols_names = ' ,'.join(cols_names)
        joins = [f"LEFT JOIN {lang}_{year}_month AS A{year} ON replace(W.{lang}_title, ' ', '_') = A{year}.article" for year in SUPPORTED_YEARS]
        str_joins = ' '.join(joins)

        sql_command = f"""
            CREATE VIEW {view_name} AS
            SELECT
                W.qid,
                W.{lang}_title,
                W.en_translation,
                {cols_names},
                W.props
            FROM
                _wikidata AS W
                {str_joins};

            """
        try:
            print(sql_command)
            cursor.execute(sql_command)
            conn.commit()
    
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de la vue : {e}")

    conn.close()
