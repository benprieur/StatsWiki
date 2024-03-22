from datetime import date

DB_NAME = 'StatsWiki00.db'
CURRENT_YEAR = 2024
SUPPORTED_YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
SUPPORTED_LANGUAGES = ['ar', 'de', 'en', 'eo', 'es', 'fr', 'ja', 'he', 'hy', 'it', 'ko', 'nl', 'pl', 'pt', 'ru', 'uk', 'zh']
SQL_LIMIT = 25
REDIRECTS_OUTPUT_FILE = "redirects.txt"

def  GET_START_END_MONTHS():
    start_date = date(2015, 7, 1)
    end_date = date.today()
    diff_months_number = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1  
    sm = start_date.month
    en = diff_months_number
    return sm, en
START_MONTH, END_MONTH = GET_START_END_MONTHS()


# Memory
REQUEST_TYPE = ['day', 'month', 'year', 'lang']
GISCARD_TRICK = '&/==+'