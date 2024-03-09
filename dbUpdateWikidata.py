from wikidata import get_qid, get_wikidata_stuff
from dbInsertLayer import insert_wikidata_stuff
from constants import SUPPORTED_YEARS, SUPPORTED_LANGUAGES
from dbRequestLayer import request_by_lang_by_date
'''
    insert_wikidata_by_lang_by_article
'''
def insert_wikidata_by_lang_by_article(lang, article):
    _, qid = get_qid(lang, article)
    if qid:
        wikidata_stuff = get_wikidata_stuff(lang, qid)
        if wikidata_stuff is not {}:
            insert_wikidata_stuff(lang, qid, wikidata_stuff)


for lang in SUPPORTED_LANGUAGES:
    response = request_by_lang_by_date(lang, 2024, 3, 8)
    #print(response)
    for tup in response:
        title = tup[1]
        print(f"{lang}-{title}")
        insert_wikidata_by_lang_by_article(lang, title)



