from wikidata import get_qid, get_wikidata_stuff
from dbInsertLayer import insert_wikidata_stuff
from constants import DB_NAME, SUPPORTED_YEARS, SUPPORTED_LANGUAGES
from constants_langs import FILTERS_BY_LANG
import sqlite3
import time

'''
    filter_results
'''
def filter_results(lang, article):
    filters = tuple(FILTERS_BY_LANG[lang]) + tuple(FILTERS_BY_LANG['global'])
    for filter in filters:
        if article.startswith(filter):
            return False
    return True


'''
    insert_wikidata_by_lang_by_article
'''
def insert_wikidata_by_lang_by_article(lang, article_tuple):
    article = article_tuple[0]
    _, qid = get_qid(lang, article)

    if filter_results(lang, article):
        wikidata_stuff = {}
        if qid == f"Q_{lang}_" + article:
            #Redir
            wikidata_stuff = { 'label_en': '', 
                            'main_properties' : {}, 
                            'sitelinks' : {} 
        }
        else:
            wikidata_stuff = get_wikidata_stuff(lang, qid)
        print(f'{qid} {article} {lang}')
        insert_wikidata_stuff(lang, qid, article, wikidata_stuff)

'''
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
article = 'محمد بن سلمان بن عبد العزيز آل سعود'
article = article.replace(" ", "_")
sql_command2 = f"SELECT * FROM _wikidata WHERE ar_title = '{article}';"
cursor.execute(sql_command2)
print(cursor.fetchall())
'''

'''
for qid in ['Q712280', 'Q6892571', 'Q355']:
    for lang in ['ar']:
        wikidata_stuff = get_wikidata_stuff(lang, qid)
        sitelinks = wikidata_stuff['sitelinks']
        article = ""
        for langwiki, site in sitelinks.items():
            lg = langwiki.replace('wiki', '')
            if lg == lang:
                article = site['title'].replace("_", " ")
                print(article)
                print(qid)
                insert_wikidata_stuff('ar', qid, article, wikidata_stuff)

'''

'''
for lang in SUPPORTED_LANGUAGES:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    sql_command2 = f"UPDATE _wikidata SET {lang}_title = REPLACE({lang}_title, ' ', '_');"
    cursor.execute(sql_command2)
    conn.commit()

    sql_command3 = f"SELECT * FROM _wikidata WHERE {lang}_title LIKE '% %';"
    cursor.execute(sql_command3)
    print(cursor.fetchall())

    conn.close()
'''

'''
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
sql_command3 = f"SELECT * FROM _wikidata WHERE qid = 'Q6892571';"
cursor.execute(sql_command3)
print(cursor.fetchall())
conn.close()
'''

for qid in ['Q124825214']:
    for lang in ['fr']:
        wikidata_stuff = get_wikidata_stuff(lang, qid)
        sitelinks = wikidata_stuff['sitelinks']
        article = ""
        for langwiki, site in sitelinks.items():
            lg = langwiki.replace('wiki', '')
            if lg == lang:
                article = site['title'].replace("_", " ")
                print(article)
                print(qid)
                insert_wikidata_stuff('ar', qid, article, wikidata_stuff)
