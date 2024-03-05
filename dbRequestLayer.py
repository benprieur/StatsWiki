import sqlite3

from constants import DB_NAME, SQL_LIMIT
from constants_wikidata import WIKIDATA_TABLE
from constants_langs import FILTERS_BY_LANG

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
def request_by_lang_by_day(lang, year, month, day):
    daily_table = f'{lang}_{year}_day'
    formatted_date = f'_{year}{month:02d}{day:02d}'

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        if table_exists(cursor, daily_table) and column_exists(conn, daily_table, formatted_date):
            sql_query = f"""
                SELECT d.article, d.{formatted_date}
                FROM {daily_table} AS d
                WHERE d.{formatted_date} IS NOT NULL
                ORDER BY d.{formatted_date} DESC
                LIMIT {SQL_LIMIT}
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
def request_by_lang_by_month(lang, year, month):
    monthly_table = f'{lang}_{year}_month'
    conn = sqlite3.connect(DB_NAME)
    formatted_date = f'_{month:02d}'
    cursor = conn.cursor()
    filtered_results = []

    try:
        if table_exists(cursor, monthly_table) and column_exists(conn, monthly_table, formatted_date):
            sql_query = f"""
                SELECT d.article, d.{formatted_date}
                FROM {monthly_table} AS d
                WHERE d.{formatted_date} IS NOT NULL
                ORDER BY d.{formatted_date} DESC
                LIMIT {SQL_LIMIT}
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
def request_by_lang_by_year(lang, year):
    yearly_table = f'{lang}_{year}'
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    filtered_results = []

    try:
        if table_exists(cursor, yearly_table) and column_exists(conn, yearly_table, 'views'):
            sql_query = f"""
                SELECT d.article, d.views
                FROM {yearly_table} AS d
                WHERE d.views IS NOT NULL
                ORDER BY d.views DESC
                LIMIT {SQL_LIMIT}
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
def request_by_lang(lang):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    view_name = f"{lang}_view"

    sql_query = f"""
        SELECT v.article, SUM(v.views) AS total_views
        FROM {view_name} AS v
        GROUP BY v.article
        ORDER BY total_views DESC
        LIMIT {SQL_LIMIT}
    """

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return filter_results(lang, results) 
    except sqlite3.Error as e:
        print(f"'{lang}' - {e}")
    finally:
        conn.close()

    return []


'''
    request_wikidata_stuff
'''
def request_wikidata_stuff(lang, articles):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    placeholders = ', '.join(['?' for _ in articles])
    select_query = f'''
    SELECT {WIKIDATA_TABLE}.qid, {WIKIDATA_TABLE}.{lang}_title, COALESCE({WIKIDATA_TABLE}.en_translation, '') AS en_translation
    FROM {WIKIDATA_TABLE}
    LEFT JOIN (
        SELECT {WIKIDATA_TABLE}.{lang}_title, {WIKIDATA_TABLE}.en_translation
        FROM {WIKIDATA_TABLE}
    ) AS translations
    ON {WIKIDATA_TABLE}.{lang}_title = translations.{lang}_title
    WHERE {WIKIDATA_TABLE}.{lang}_title IN ({placeholders})
    '''

    cursor.execute(select_query, articles)
    results = cursor.fetchall()
    conn.close()
    return results


'''
    request_wikidata_stuff_by_article
'''
def request_wikidata_stuff_by_article(lang, article):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    select_query = f'''
    SELECT *
    FROM {WIKIDATA_TABLE}
    WHERE {WIKIDATA_TABLE}.{lang}_title = ?
    '''

    cursor.execute(select_query, (article,))
    wikidata_stuff = cursor.fetchall()
    conn.close()
    return wikidata_stuff