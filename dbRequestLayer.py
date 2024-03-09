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
def request_by_lang_by_articles_by_date(lang, articles, year=0, month=0, day=0):
    if lang not in SUPPORTED_LANGUAGES:
        return []

    if year not in SUPPORTED_YEARS:
        return []

    if (month not in range(1, 13) and month != 0) or (day not in range(1, 32) and day != 0):
        return []

    formatted_articles = [article.replace(" ", "_") for article in articles]
    placeholders = ', '.join('?' for _ in formatted_articles)  

    col_date = ""
    if day > 0:
        col_date = f"_{year}{month:02d}{day:02d}"
    elif month > 0:
        col_date = f"_{month:02d}"
    else:
        col_date = "views"

    sql_query = f"""
        SELECT
            qid,
            {lang}_title,
            en_translation,
            props,
            {col_date}
        FROM
            {lang}_{year}_vue
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
def request_by_lang_by_qids_by_date(lang, qids, year=0, month=0, day=0):
    if lang not in SUPPORTED_LANGUAGES:
        return []

    if year not in SUPPORTED_YEARS:
        return []

    if (month not in range(1, 13) and month != 0) or (day not in range(1, 32) and day != 0):
        return []

    placeholders = ', '.join('?' for _ in qids)  

    col_date = ""
    if day > 0:
        col_date = f"_{year}{month:02d}{day:02d}"
    elif month > 0:
        col_date = f"_{month:02d}"
    else:
        col_date = "views"

    sql_query = f"""
        SELECT
            qid,
            {lang}_title,
            en_translation,
            props,
            {col_date}
        FROM
            {lang}_{year}_vue
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
        print(f"Error in request_by_lang_by_articles_by_date: {e}")
        return []
    finally:
        conn.close()


'''
    request_by_lang_by_date
'''
def request_by_lang_by_date(lang, year=0, month=0, day=0):
    
    if lang not in SUPPORTED_LANGUAGES:
        return []
    if year not in SUPPORTED_YEARS and year != 0:
        return []
    if (month not in range(1, 13)) and month != 0:
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
                FROM {lang}_{year}_vue
                WHERE {col_day} IS NOT NULL
                ORDER BY {col_day} DESC
                LIMIT {SQL_LIMIT};
            """
    elif year and month and day == 0:
        col_month = f'_{month:02d}'
        sql_query = f"""
                SELECT
                qid,
                {lang}_title,
                en_translation,
                props,
                {col_month}
                FROM {lang}_{year}_vue
                WHERE {col_month} IS NOT NULL
                ORDER BY {col_month} DESC
                LIMIT {SQL_LIMIT};
            """
    elif year and month == 0 and day == 0:
        sql_query = f"""
                SELECT
                qid,
                {lang}_title,
                en_translation,
                props,
                views
                FROM {lang}_{year}_vue
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
        print(sql_query)
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
        print(sql_query)
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return filter_results(lang, results)
    except Exception as e:
        print(e)
        return []
    finally:
        conn.close()

'''
    special_request_redirects
'''
def special_request_redirects(lang, redirects, year=0, month=0, day=0):
    
    if lang not in SUPPORTED_LANGUAGES:
        return []
    if year not in SUPPORTED_YEARS and year != 0:
        return []
    if (month not in range(1, 13)) and month != 0:
        return []

    redirects = [redirect.replace(" ", "_") for redirect in redirects]           
    placeholders = ', '.join('?' for _ in redirects)  
    
    if year and month and day:
        col_day = f'_{year}{month:02d}{day:02d}'
        sql_query = f"""
            SELECT
            {col_day}
            FROM {lang}_{year}_day
            WHERE article IN ({placeholders});
            """
    
    elif year and month and day == 0:
        col_month = f'_{month:02d}'
        sql_query = f"""
            SELECT
            {col_month}
            FROM {lang}_{year}_month
            WHERE article IN ({placeholders});
            """

    elif year and month == 0 and day == 0:
        sql_query = f"""
            SELECT
            views
            FROM {lang}_{year}
            WHERE article IN ({placeholders});
            """
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query, redirects)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f'redirects query: {e}')
        return []
    finally:
        conn.close()