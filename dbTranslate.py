import sqlite3
from GlobalData import DB_NAME

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
create_table_query = '''
CREATE TABLE IF NOT EXISTS Translation (
    lang TEXT NOT NULL,
    article TEXT NOT NULL,
    translation TEXT NOT NULL
);
'''
cursor.execute(create_table_query)