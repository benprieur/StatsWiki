import sqlite3

from constants import DB_NAME, SQL_LIMIT, SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from constants_wikidata import WIKIDATA_TABLE
from constants_langs import FILTERS_BY_LANG

'''
    filter_results
'''
def filter_results(lang, results):
    filters = tuple(FILTERS_BY_LANG[lang]) + tuple(FILTERS_BY_LANG['global'])
    results = [result for result in results if not result[1].startswith(filters)]
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
    request_by_lang_by_articles_by_date
'''
def request_by_lang_by_articles_by_date(lang, articles, year, month=0, day=0):
    if lang not in SUPPORTED_LANGUAGES:
        return []

    if year not in SUPPORTED_YEARS:
        return []

    formatted_articles = [article.replace(" ", "_") for article in articles]
    placeholders = ', '.join('?' for _ in formatted_articles)  

    col_date = ""
    view_name = f"{lang}_{year}_vue"
    if day:
        col_date = f"_{year}{month:02d}{day:02d}"
        view_name = f'{lang}_{year}_day_view'
    elif month:
        col_date = f"_{month:02d}"
        view_name = f'{lang}_{year}_month_view'
    else:
        col_date = "views"
        view_name = f'{lang}_{year}_view'

    sql_query = f"""
        SELECT
            qid,
            {lang}_title,
            en_translation,
            props,
            {col_date}
        FROM
            {view_name}
        WHERE
            {lang}_title IN ({placeholders})
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query, formatted_articles)
        results = cursor.fetchall()
        return filter_results(lang, results)
    except Exception as e:
        print(f"Error in request_by_lang_by_articles_by_date: {e}")
        return []
    finally:
        conn.close()


'''
    request_by_lang_by_qids_by_date
'''
def request_by_lang_by_qids_by_date(lang, qids, year, month=0, day=0):

    if lang not in SUPPORTED_LANGUAGES:
        return []

    if year not in SUPPORTED_YEARS:
        return []

    placeholders = ', '.join('?' for _ in qids)

    col_date = ""
    view_name = ""
    if day and month and year:
        col_date = f"_{year}{month:02d}{day:02d}"
        view_name = f"{lang}_{year}_day_view"
    elif month and year:
        col_date = f"_{month:02d}"
        view_name = f'{lang}_{year}_month_view'
    elif year:
        col_date = "views"
        view_name = f'{lang}_{year}_view'

    sql_query = f"""
        SELECT
            qid,
            {lang}_title,
            en_translation,
            props,
            {col_date}
        FROM
            {view_name}
        WHERE
            qid IN ({placeholders})
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query, qids)
        results = cursor.fetchall()
        return filter_results(lang, results)
    except Exception as e:
        print(f"request_by_lang_by_qids_by_date: {e}")
        return []
    finally:
        conn.close()


'''
    request_by_lang_by_date
'''
def request_by_lang_by_date(lang, year, month=0, day=0):
    
    if lang not in SUPPORTED_LANGUAGES:
        return []
    if year not in SUPPORTED_YEARS:
        return []
    
    sql_query = ""
    
    if year and month and day:
        col_day = f'_{year}{month:02d}{day:02d}'
        sql_query = f"""
                SELECT
                qid,
                {lang}_title,
                en_translation,
                props,
                {col_day}
                FROM {lang}_{year}_day_view
                WHERE {col_day} IS NOT NULL
                ORDER BY {col_day} DESC
                LIMIT {SQL_LIMIT};
            """
    elif year and month:
        col_month = f'_{month:02d}'
        sql_query = f"""
                SELECT
                qid,
                {lang}_title,
                en_translation,
                props,
                {col_month}
                FROM {lang}_{year}_month_view
                WHERE {col_month} IS NOT NULL
                ORDER BY {col_month} DESC
                LIMIT {SQL_LIMIT};
            """
    elif year:
        sql_query = f"""
                SELECT
                qid,
                {lang}_title,
                en_translation,
                props,
                views
                FROM {lang}_{year}_view
                WHERE views IS NOT NULL
                ORDER BY views DESC
                LIMIT {SQL_LIMIT};
            """
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return filter_results(lang, results)
    except Exception as e:
        print(f'request_by_lang_by_date: {e}')
        return []
    finally:
        conn.close()


'''
    request_by_qid
'''
def request_by_qid(lang, qid_):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if lang not in SUPPORTED_LANGUAGES:
        return []
    
    sql_query = f"""
                SELECT
                qid,
                {lang}_title,
                en_translation,
                props
                FROM {lang}_vue
                WHERE qid='{qid_}'
            """
    
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return filter_results(lang, results)
    except Exception as e:
        print(f'request_by_qid: {e}')
    finally:
        if conn:
            conn.close()


'''
    request_by_lang
'''
def request_by_lang(lang):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    view_name = f'{lang}_vue'
    
    sum_months = " + ".join([f"_{year}{month:02d}" for year in SUPPORTED_YEARS for month in range(1, 13)])


    sql_query = f"""
                SELECT
                qid,
                {lang}_title,
                en_translation,
                props,
                {sum_months} AS views
                FROM {view_name}
                ORDER BY views DESC
                LIMIT {SQL_LIMIT};
            """

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return filter_results(lang, results)
    except Exception as e:
        print(e)
        return []
    finally:
        conn.close()

'''
    request_dataviz
'''
def request_dataviz(lang, qid_):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    view_name = f'{lang}_vue'
    
    months = ", ".join([f"_{year}{month:02d}" for year in SUPPORTED_YEARS for month in range(1, 13)])

    sql_query = f"""
                SELECT
                qid,
                {lang}_title,
                en_translation,
                props,
                {months}
                FROM {view_name}
                WHERE qid='{qid_}';
            """

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return filter_results(lang, results)
    except Exception as e:
        print(e)
        return []
    finally:
        conn.close()

'''
    special_request_redirect
'''
def special_request_redirect(lang, redirect, year, month=0, day=0):

    redirect = redirect.replace(" ", "_")

    if year and month and day:
        col_day = f'_{year}{month:02d}{day:02d}'
        table_day = f"{lang}_{year}_day"
        sql_query = f"""
            SELECT
            {col_day}
            FROM {table_day}
            WHERE article = "{redirect}";
            """
    
    elif year and month:
        col_month = f'_{month:02d}'
        table_month = f"{lang}_{year}_month"
        sql_query = f"""
            SELECT
            {col_month}
            FROM {table_month}
            WHERE article = "{redirect}";
            """

    elif year:
        col_year = f'views'
        table_year = f"{lang}_{year}"
        sql_query = f"""
            SELECT
            {col_year}
            FROM {table_year}
            WHERE article = "{redirect}";
            """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f'special_request_redirect query: {e}')
        return []
    finally:
        conn.close()