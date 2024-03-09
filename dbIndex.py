import sqlite3
from constants import DB_NAME, SUPPORTED_LANGUAGES

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
