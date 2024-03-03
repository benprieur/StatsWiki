import sqlite3
from GlobalData import DB_NAME, FILTERS_BY_LANG

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

def request_data_date_lang(lang, yy, mm, dd):
    daily_table = f'{lang}_{yy}_day'

    conn = sqlite3.connect(DB_NAME)
    formatted_date = f'_{yy}{mm}{dd}'
    cursor = conn.cursor()
    filtered_results = []
    if table_exists(cursor, daily_table): 
        if column_exists(conn, daily_table, formatted_date): 
            sql_query = f"SELECT article, {formatted_date} FROM {daily_table} ORDER BY {formatted_date} DESC LIMIT 50"
            cursor.execute(sql_query)
            results = cursor.fetchall()
            filtered_results = filter_results(lang, results)
            conn.close()
    return filtered_results


def request_data_month_lang(lang, yy, mm):
    monthly_table = f'{lang}_{yy}_month'
    conn = sqlite3.connect(DB_NAME)
    formatted_date = f'_{mm}'
    cursor = conn.cursor()
    filtered_results = []
    if table_exists(cursor, monthly_table):
        if column_exists(conn, monthly_table, formatted_date):  
            sql_query = f"SELECT article, {formatted_date} FROM {monthly_table} ORDER BY {formatted_date} DESC LIMIT 50"
            cursor.execute(sql_query)
            results = cursor.fetchall()
            filtered_results = filter_results(lang, results)
            conn.close()    
    return filtered_results


def request_data_year_lang(lang, year):
    yearly_table = f'{lang}_{year}'
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    filtered_results = []
    if table_exists(cursor, yearly_table):
        if table_exists(cursor, yearly_table): 
            sql_query = f"SELECT article, views FROM {yearly_table} ORDER BY views DESC LIMIT 50"
            cursor.execute(sql_query)
            results = cursor.fetchall()
            filtered_results = filter_results(lang, results)
            conn.close()
    return filtered_results

def get_articles_ranking_by_lang(lang):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    view_name = f"{lang}_view"

    ranking_query = f"""
    SELECT article, SUM(views) AS total_views
    FROM {view_name}
    GROUP BY article
    ORDER BY total_views DESC LIMIT 50;
    """

    try:
        cursor.execute(ranking_query)
        results = cursor.fetchall()
        filtered_results = filter_results(lang, results)
        return filtered_results
    except sqlite3.Error as e:
        print(f"'{lang}' - {e}")
    finally:
        conn.close()

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
