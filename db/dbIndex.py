import sqlite3
from const.constants import DB_NAME, SUPPORTED_LANGUAGES, SUPPORTED_YEARS

def index_wikidata_qid():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    sql_command = "CREATE INDEX index_wikidata_qid ON _wikidata (qid);"
    try:
        cursor.execute(sql_command)
    except sqlite3.Error as e:
        print(f"{e}")

    conn.commit()
    conn.close()

def index_wikidata_titles():

    cols = [    'ar_title', 
                'de_title',  
                'en_title',  
                'eo_title',  
                'es_title',  
                'fr_title',  
                'ja_title',  
                'he_title',  
                'hy_title',  
                'it_title',  
                'ko_title',  
                'nl_title',  
                'pl_title',  
                'pt_title',  
                'ru_title',  
                'uk_title',  
                'zh_title' 
            ]

    for col in cols :    

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        sql_command = f"""
            CREATE INDEX index_{col} ON _wikidata ({col});
        """
    
        try:
            cursor.execute(sql_command)
        except sqlite3.Error as e:
            print(f"{e}")

        conn.commit()
        conn.close()

'''
    index_tables_times
'''
def index_tables_times():


    for lang in SUPPORTED_LANGUAGES:
        for year in SUPPORTED_YEARS:

            table_day = f"{lang}_{year}_day"
            table_month = f"{lang}_{year}_month"
            table_year = f"{lang}_{year}"

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
    
            sql_command_year = f"""
                CREATE INDEX index_{lang}_{year} ON {table_year}(article);
            """

            try:
                cursor.execute(sql_command_year)
                conn.commit()
            except Exception as e:
                print(e)

            
            conn.close()
            
            ####### END YEAR
            
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            sql_command_month= f"""
                CREATE INDEX index_{lang}_{year}_month ON {table_month}(article);
            """

            try:
                cursor.execute(sql_command_month)
                conn.commit()
            except Exception as e:
                print(e)
                
            conn.close()

            #### END MONTH 

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            sql_command_day= f"""
                CREATE INDEX index_{lang}_{year}_day ON {table_day}(article);
            """

            try:
                cursor.execute(sql_command_day)
                conn.commit()
            except Exception as e:
                print(e)

            conn.close()

index_tables_times()