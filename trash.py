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

#wikidata_stuff = get_wikidata_stuff('uk', 'Q485500')
#insert_wikidata_stuff('uk', 'Q485500', "", wikidata_stuff)