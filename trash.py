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
sql_command3 = f"SELECT * FROM zh_2020_view;"
cursor.execute(sql_command3)
print(cursor.fetchall())
conn.close()
'''

'''
# Définition des entêtes pour simuler un navigateur
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "DNT": "1",  # Do Not Track Request Header
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}

SUPPORTED_LANGUAGES = ['ar', 'az', 'de', 'en', 'eo', 'es', 'fr', 'ja', 'he', 'hy', 'it', 'ko', 'nl', 'pl', 'pt', 'ru', 'uk', 'zh']
import requests
for lang in SUPPORTED_LANGUAGES:
        
        # all
        url = "https://statswiki.info/api/"  + lang
        response = requests.get(url, headers=headers)
        print(response)
        print("all ok")

        # year
        url = "https://statswiki.info/api/"  + lang + "/2024"
        response = requests.get(url, headers=headers)
        print("year ok")

        # month
        url = "https://statswiki.info/api/"  + lang + "/2024/04"
        response = requests.get(url, headers=headers)
        print("month ok")

        # day
        url = "https://statswiki.info/api/"  + lang + "/2024/04/01"
        response = requests.get(url, headers=headers)
        print("day ok")
'''

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
sql_command2 = f"SELECT qid, az_title,en_translation, props, _20190303 FROM az_2019_day_view WHERE _20190303 IS NOT NULL ORDER BY _20190303 DESC LIMIT 56;"
cursor.execute(sql_command2)
print(cursor.fetchall())

                
                
                
                
                
                
                