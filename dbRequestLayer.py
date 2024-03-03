import sqlite3
from constants import DB_NAME, FILTERS_BY_LANG

'''
    filter_results
'''
def filter_results(lang, results):
    filters = tuple(FILTERS_BY_LANG[lang]) + tuple(FILTERS_BY_LANG['common'])
    results = [result for result in results if not result[0].startswith(filters)]
    return results


'''
    table_exists
'''
def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cursor.fetchone() is not None


'''
    column_exists
'''
def column_exists(conn, table_name, column_name):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns_info = cursor.fetchall()
    for col_info in columns_info:
        if col_info[1] == column_name:
            return True
    return False


'''
    request_by_lang_by_day
'''
def request_by_lang_by_day(lang, year, month, day, translation=True):
    daily_table = f'{lang}_{year}_day'
    formatted_date = f'_{year}{month:02d}{day:02d}'

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        if table_exists(cursor, daily_table) and column_exists(conn, daily_table, formatted_date):
            sql_query = f"""
                SELECT d.article, d.{formatted_date}{", t.translation" if translation else ""}
                FROM {daily_table} AS d
                {f"LEFT JOIN Translation AS t ON d.article = t.article AND t.lang = '{lang}'" if translation else ""}
                WHERE d.{formatted_date} IS NOT NULL
                ORDER BY d.{formatted_date} DESC
                LIMIT 50
            """
            cursor.execute(sql_query)
            results = cursor.fetchall()
            filtered_results = filter_results(lang, results)
            return filtered_results
    finally:
        conn.close()

    return []






'''
    request_by_lang_by_month
'''
def request_by_lang_by_month(lang, year, month, translation=True):
    monthly_table = f'{lang}_{year}_month'
    conn = sqlite3.connect(DB_NAME)
    formatted_date = f'_{month:02d}'
    cursor = conn.cursor()
    filtered_results = []

    try:
        if table_exists(cursor, monthly_table) and column_exists(conn, monthly_table, formatted_date):
            sql_query = f"""
                SELECT d.article, d.{formatted_date}{", t.translation" if translation else ""}
                FROM {monthly_table} AS d
                {f"LEFT JOIN Translation AS t ON d.article = t.article AND t.lang = '{lang}'" if translation else ""}
                WHERE d.{formatted_date} IS NOT NULL
                ORDER BY d.{formatted_date} DESC
                LIMIT 50
            """
            cursor.execute(sql_query)
            results = cursor.fetchall()
            filtered_results = filter_results(lang, results)
            return filtered_results
    finally:
        conn.close()

    return []


'''
    request_by_lang_by_month
'''
def request_by_lang_by_year(lang, year, translation=True):
    yearly_table = f'{lang}_{year}'
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    filtered_results = []

    try:
        if table_exists(cursor, yearly_table) and column_exists(conn, yearly_table, 'views'):
            sql_query = f"""
                SELECT d.article, d.views{", t.translation" if translation else ""}
                FROM {yearly_table} AS d
                {f"LEFT JOIN Translation AS t ON d.article = t.article AND t.lang = '{lang}'" if translation else ""}
                WHERE d.views IS NOT NULL
                ORDER BY d.views DESC
                LIMIT 50
            """
            cursor.execute(sql_query)
            results = cursor.fetchall()
            filtered_results = filter_results(lang, results)
            return filtered_results
    finally:
        conn.close()

    return []


'''
    def request_by_lang
'''
def request_by_lang(lang, translation=True):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    view_name = f"{lang}_view"

    # Construire la requête SQL en tenant compte de la demande de traduction
    sql_query = f"""
        SELECT v.article, SUM(v.views) AS total_views{", t.translation" if translation else ""}
        FROM {view_name} AS v
        {f"LEFT JOIN Translation AS t ON v.article = t.article AND t.lang = '{lang}'" if translation else ""}
        GROUP BY v.article
        ORDER BY total_views DESC LIMIT 50;
    """

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        # Pas besoin de filtrer les résultats ici si 'filter_results' est spécifique à la structure des données
        filtered_results = filter_results(lang, results) if translation else results
        return filtered_results
    except sqlite3.Error as e:
        print(f"'{lang}' - {e}")
    finally:
        conn.close()

    return []


'''
    get_translation
'''
def get_translation(article, lang):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    request = """SELECT translation FROM Translation
             WHERE lang = ?
             AND article = ?"""

    
    params = (lang, article)

    try:
        cursor.execute(request, params)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"'{lang}' - {e}")
    finally:
        conn.close()
