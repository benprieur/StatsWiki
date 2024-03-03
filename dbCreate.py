import sqlite3
from datetime import date, timedelta
from constants import DB_NAME
import calendar

def CreateTables(years, langs):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()    

    for lang in langs:
        for year in years:

            start_date = date(year, 1, 1)
            number_days_by_year =  365
            if calendar.isleap(year):
                number_days_by_year = 366

            day_columns = [start_date + timedelta(days=i) for i in range(number_days_by_year)]
            day_column_names = [f"_{day.year}{day.month:02d}{day.day:02d}" for day in day_columns]

            table_name_day = f'{lang}_{year}_day'
            columns_definition_day = ", ".join(f"{day} INTEGER DEFAULT 0" for day in day_column_names)
            create_table_query_day = f"""
            CREATE TABLE IF NOT EXISTS {table_name_day} (
                article TEXT PRIMARY KEY,
                {columns_definition_day}
            );
            """

            table_name_month = f'{lang}_{year}_month'
            columns_definition_month = " INTEGER DEFAULT 0, ".join([f"_{month:02d}" for month in range(1, 13)]) + " INTEGER DEFAULT 0"
            create_table_query_month = f"""
            CREATE TABLE IF NOT EXISTS {table_name_month} (
                    article TEXT PRIMARY KEY,
                    {columns_definition_month}
            );
            """

            table_name_year = f'{lang}_{year}'
            create_table_query_year = f"""
            CREATE TABLE IF NOT EXISTS {table_name_year} (
                    article TEXT PRIMARY KEY,
                    views
            );
            """

            try:
                cursor.execute(create_table_query_day)
                conn.commit()
                cursor.execute(create_table_query_month)
                conn.commit()
                cursor.execute(create_table_query_year)
                conn.commit()
            except sqlite3.Error as e:
                print(f"{e}")

    conn.close()


if __name__ == '__main__':
    years = []
    langs = []
    CreateTables(years, langs)