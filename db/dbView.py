import sqlite3
DB_NAME = '../StatsWiki00.db'
SUPPORTED_YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
from datetime import timedelta, date
import calendar

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

'''
    create_views_day
'''
def create_views_day():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for lang in ['az']:
        for year in SUPPORTED_YEARS:
            view_name = f"{lang}_{year}_day_view"  

            start_date = date(year, 1, 1)
            number_days_by_year =  365
            if calendar.isleap(year):
                number_days_by_year = 366

            day_columns = [start_date + timedelta(days=i) for i in range(number_days_by_year)]
            day_column_names = ', '.join([f"D._{day.year}{day.month:02d}{day.day:02d}" for day in day_columns])


            sql_command = f"""
                CREATE VIEW {view_name} AS
                SELECT
                    W.qid,
                    W.{lang}_title,
                    W.en_translation,
                    {day_column_names},
                    W.props
                FROM
                    _wikidata AS W
                JOIN {lang}_{year}_day AS D ON replace(W.{lang}_title, ' ', '_') = D.article;
                """
            try:
                #print(sql_command)
                cursor.execute(sql_command)
                conn.commit()
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

    conn.close()

'''
    create_views_month
'''
def create_views_month():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for lang in ['az']:
        for year in SUPPORTED_YEARS:
            view_name = f"{lang}_{year}_month_view"  

            sql_command = f"""
                CREATE VIEW {view_name} AS
                SELECT
                    W.qid,
                    W.{lang}_title,
                    W.en_translation,
                    M._01,
                    M._02,     
                    M._03,
                    M._04,     
                    M._05,
                    M._06,     
                    M._07,
                    M._08,
                    M._09,
                    M._10,
                    M._11,
                    M._12,                    
                    W.props
                FROM
                    _wikidata AS W
                JOIN {lang}_{year}_month AS M ON replace(W.{lang}_title, ' ', '_') = M.article;
                """
            try:
                print(sql_command)
                cursor.execute(sql_command)
                conn.commit()
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

    conn.close()


'''
    create_views_year
'''
import sqlite3

def create_views_year():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for lang in ['az']:
        for year in SUPPORTED_YEARS:
            view_name = f"{lang}_{year}_view"  

            sql_command = f"""
                CREATE VIEW {view_name} AS
                SELECT
                    W.qid,
                    W.{lang}_title,
                    W.en_translation,
                    Y.views,
                    W.props
                FROM
                    _wikidata AS W
                JOIN {lang}_{year} AS Y ON replace(W.{lang}_title, ' ', '_') = Y.article;
                """
            try:
                print(sql_command)
                cursor.execute(sql_command)
                conn.commit()
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

    conn.close()


'''
    create_views_alltime
'''
def create_views_alltime():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for lang in ['az']:
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

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

#sql_command1 = "UPDATE _wikidata SET fr_title = 'Cédric_Doumbè' WHERE qid = 'Q24452252';"
#cursor.execute(sql_command1)
#conn.commit()

#sql_command2 = "SELECT * FROM fr_2024 WHERE article = 'Cédric_Doumbé';"
#cursor.execute(sql_command2)
#print(cursor.fetchall())


create_views_day()
create_views_month()
create_views_year()
create_views_alltime()