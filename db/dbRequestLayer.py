import sqlite3
from const.constants import DB_NAME, SUPPORTED_LANGUAGES, SUPPORTED_YEARS, SQL_LIMIT
from const.FILTERS_BY_LANG import FILTERS_BY_LANG
from const.SUPPORTED_REDIRECTS_BY_LANG import SUPPORTED_REDIRECTS_BY_LANG
from const.FILTERERED_QIDS import FILTERERED_QIDS
from objects import Lines, Line
from commons import get_commons_image_url
from wikimedia import get_first_sentence_wikipedia_article
import json

'''
    image, image_url = dumps_properties(props)   
'''
def dumps_properties(props):
        
    props_str = json.dumps(props)
    wikidata_image, wikidata_image_url = '', ''
    if props_str != 'null':
        wikidata_image = get_value_from_string_by_key(props_str, "P18")
        wikidata_image_url =  ""
        if wikidata_image:
            wikidata_image_url = 'https://commons.wikimedia.org/wiki/File:' + wikidata_image.replace(' ', '_')
            wikidata_image = get_commons_image_url(wikidata_image_url)
    
    return wikidata_image, wikidata_image_url

'''
    build_answer
'''
def build_answer(lang, results, sequence, year=0, month=0, day=0):
    
    FILTERS = FILTERS_BY_LANG[lang] + FILTERS_BY_LANG['global']
    lines = Lines(lang, year, month, day)

    try:
        for result in results:

            line = Line()

            for index, element in enumerate(sequence):
                if element == 'qid':
                    line.qid = result[index]
                elif element == 'title':
                    line.title = result[index]
                elif element == 'en_translation':
                    line.en_translation = result[index]
                elif element == 'views':
                    line.views = result[index]
                elif element == 'props':
                    line.props = result[index]
                    line.wikidata_image, line.wikidata_image_url = dumps_properties(line.props)
                elif element == 'views_collection':
                    line.views_collection = result[index:]
            if not line.title_with_undescores.startswith(FILTERS) and not line.qid in FILTERERED_QIDS.keys() and not line.title_with_spaces in SUPPORTED_REDIRECTS_BY_LANG[lang].keys():
                lines.add(line)

        return lines
    
    except Exception as e:
        print(f"Error in build_answer: {e}")
        return Lines(lang)


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
        return build_answer(lang, results, ['qid', 'title', 'en_translation', 'props', 'views'], year, month, day)
    
    except Exception as e:
        print(f"Error in request_by_lang_by_articles_by_date: {e}")
        return []
    finally:
        conn.close()


'''
    request_qid_from_wikidata_table
'''
def request_qid_from_wikidata_table(lang, qid):
   
    sql_query = f"SELECT qid, {lang}_title, en_translation, props FROM _wikidata WHERE qid = '{qid}';"
   
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return build_answer(lang, results, ['qid', 'title', 'en_translation', 'props'])
    except Exception as e:
        print(f"request_qid_from_wikidata_table: {e}")
        return []
    finally:
        conn.close()


'''
    request_by_lang_by_qid_by_date
'''
def request_by_lang_by_qid_by_date(lang, qid_, year, month=0, day=0):

    if lang not in SUPPORTED_LANGUAGES:
        return []

    if year not in SUPPORTED_YEARS:
        return []

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
            qid = '{qid_}'
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return build_answer(lang, results, ['qid', 'title', 'en_translation', 'props', 'views'], year, month, day)
    except Exception as e:
        print(f"request_by_lang_by_qid_by_date: {e}")
        return []
    finally:
        conn.close()


'''
    request_by_lang_by_date
'''
def request_by_lang_by_date(lang, year, month=0, day=0):
        
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
        print(f'request_by_lang_by_date')
        return build_answer(lang, results, ['qid', 'title', 'en_translation', 'props', 'views'], year, month, day)
    except Exception as e:
        print(f'request_by_lang_by_date: {e}')
        return []
    finally:
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
        return build_answer(lang, results, ['qid', 'title', 'en_translation', 'props', 'views'])
    except Exception as e:
        print(f"request_by_lang {e}")
        return []
    finally:
        conn.close()

'''
    get_value_from_string_by_key
'''
def get_value_from_string_by_key(str_analyze, key):
    # "\"{\\\"P18\\\": \\\"Dark vignette Al-Masjid AL-Nabawi Door800x600x300.jpg\\\", \\\"P21\\\": \\\"Q6581097\\\", \\\"P31\\\": \\\"Q5\\\"}\"" 
 
    start_index = str_analyze.find(key)
    start_value = str_analyze.find(":", start_index)
    start_delim = str_analyze.find("\"", start_value)
    end_delim = str_analyze.find("\"", start_delim+1)
    result = str_analyze[start_delim+1:end_delim]
    result = result.replace ("\\", "")

    return result


'''
    request_monthly_views
'''
def request_monthly_views(lang, qid):

    view_name = f'{lang}_vue'
    months_ = ", ".join([f"_{year}{month:02d}" for year in SUPPORTED_YEARS for month in range(1, 13)])

    sql_query = f"""
                SELECT
                qid,
                {lang}_title,
                en_translation,
                props,
                {months_}
                FROM {view_name}
                WHERE qid='{qid}';
            """

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()

        return build_answer(lang, results, ['qid', 'title', 'en_translation', 'props', 'views_collection'])
    except Exception as e:
        print(f"request_monthly_views {e}")
        return []
    finally:
        conn.close()


'''
    request_monthly_views_redirect
'''
def request_monthly_views_redirect(lang, title):

    dict_results = {} # toutes les views par mois pour title
    for year in SUPPORTED_YEARS:

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        table_name = f"{lang}_{year}_month" 
        months_col = ", ".join([f"_{month:02d}" for month in range(1, 13)])

        query = f"SELECT {months_col} FROM {table_name} WHERE article = '{title}';"
    
        list_dict_keys = [f"{year}-{month:02d}" for month in range(1, 13)] 
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()

            if results:
                results = results[0]

                for _, (key, val) in enumerate(zip(list_dict_keys, results)):
                    dict_results[key] = val
            else:
                for key in list_dict_keys:
                    dict_results[key] = None
        except Exception as e:
            print(f"Exception request_monthly_views_redirect {e}")
            for key in list_dict_keys:
                dict_results[key] = None
        finally:
            conn.close()
    return dict_results


'''
    request_by_lang_by_qid (request_dataviz)
'''
def request_by_lang_by_qid(lang, qid):

    statistics_global = {}
    statistics = {} # Statistics, main article
    lines = request_monthly_views(lang, qid)
    line = lines.items[0]

    month_column_list = [f'{year}-{month:02d}' for year in SUPPORTED_YEARS for month in range(1,13)]

    sentence = get_first_sentence_wikipedia_article(lang, line.title)

    for index, month in enumerate(month_column_list):
        statistics[f'{month}'] = line.views_collection[index]
    
    statistics_global[f'{line.title_with_spaces}'] = statistics

    # Statistics, redirects
    for redir, qid_ in SUPPORTED_REDIRECTS_BY_LANG[lang].items():
        if qid == qid_:
            redir = redir.replace(" ", "_")
            dict_results = request_monthly_views_redirect(lang, redir.replace("'", "''"))
            statistics_global[f'{redir.replace("_", " ")}'] = dict_results

    # On remplace tout None par 0
    for title, values in statistics_global.items():
        for month, value in values.items():
            if value is None:
                values[month] = 0


    # On met à jour le 'global' avec les données des redirects
    main_dict = statistics_global[f'{line.title_with_spaces}']
    for redirect, _ in statistics_global.items():
        if redirect != line.title:
            for month, value in statistics_global[redirect].items():
                try:
                    main_dict[month] += value
                except:
                    main_dict[month] = value

    # On remplace tout 0 par None
    for title, values in statistics_global.items():
        for month, value in values.items():
            if not value:
                values[month] = None

    results_dict = {
        'lang'  : lang,
        'title' : line.title,
        'en_translation' : line.en_translation,
        'wikidata_image' : line.wikidata_image,
        'wikidata_image_url' :line.wikidata_image_url,
        'sentence' : sentence,
        'statistics_global' : statistics_global
    }
    print(results_dict)
    return results_dict


'''
    special_request_redirect
'''
def special_request_redirect(lang, redirect, year, month=0, day=0):

    redirect = redirect.replace(" ", "_")
    sql_query = f""""""

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
        return build_answer(lang, results, ['views'], year, month, day)

    except Exception as e:
        print(f'special_request_redirect query: {e}')
        return None
    finally:
        conn.close()