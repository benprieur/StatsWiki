from wikidata import get_qid, get_wikidata_stuff
from db.dbInsertLayer import insert_wikidata_stuff
from const.constants import DB_NAME, SUPPORTED_YEARS, SUPPORTED_LANGUAGES
from const.FILTERS_BY_LANG import FILTERS_BY_LANG
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

#insert_wikidata_by_lang_by_article('fr', ('Michel_Manouchian',) )
    
''''
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
sql_command2 = f"SELECT * FROM _wikidata WHERE en_translation like '%Steak%';"
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

'''
for qid in ['Q355']:
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
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
sql_command3 = f"SELECT * FROM fr_vue WHERE fr_title = 'Michel_Manouchian';"
cursor.execute(sql_command3)
print(cursor.fetchall())
conn.close()
'''

lst = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0, 0, 70996, 845115, 437092, 224042, 160286, 127521, 119941, 145025, 163423, 116742, 129340, 131648, 141891, 89003, 78330, 61426, 62580, 55420, 34990, 39712, 55670, 63755, 71272, 26468, 24111, 14415, 17855, 7110, 0, 1334, 0, 1180, 0, 4803, 0, 0, 0, 0, 2591, 0, 0, 0, 0, 0, 0, 0, 0, 1468, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
print(len(lst))