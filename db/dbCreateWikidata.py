import sqlite3
from const.constants import DB_NAME

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
create_table_query = '''
CREATE TABLE IF NOT EXISTS _wikidata (
    qid TEXT PRIMARY KEY,
    en_translation TEXT,

    ar_title TEXT,
    de_title TEXT,
    en_title TEXT,
    eo_title TEXT,
    es_title TEXT,
    fr_title TEXT,
    ja_title TEXT,
    he_title TEXT,
    hy_title TEXT,
    it_title TEXT,
    ko_title TEXT,
    nl_title TEXT,
    pl_title TEXT,
    pt_title TEXT,
    ru_title TEXT,
    uk_title TEXT,
    zh_title TEXT,
       
    props TEXT
);
'''
cursor.execute(create_table_query)
conn.commit()
conn.close()