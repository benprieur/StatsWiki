from wikidata import get_qid, get_wikidata_stuff
from dbInsertLayer import insert_wikidata_stuff
from dbRequestLayer import request_by_lang_by_year, request_by_lang_by_month, request_by_lang
from constants import SUPPORTED_YEARS, SUPPORTED_LANGUAGES

'''
    insert_wikidata_by_lang_by_article
'''
def insert_wikidata_by_lang_by_article(lang, article):
    _, qid = get_qid(lang, article)
    if qid:
        wikidata_stuff = get_wikidata_stuff(lang, qid)
        if wikidata_stuff is not {}:
            insert_wikidata_stuff(lang, qid, wikidata_stuff)

for lang in ['uk', 'ko', 'nl', 'pt', 'pl', 'zh']:
      
    articles = request_by_lang(lang)
    for article in articles:
        insert_wikidata_by_lang_by_article(lang, article[0])
        print(f'{lang}-{article[0]}')