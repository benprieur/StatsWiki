from wikidata import get_qid, get_wikidata_stuff
from dbInsertLayer import insert_wikidata_stuff
from constants import SUPPORTED_YEARS, SUPPORTED_LANGUAGES
from dbRequestLayer import request_by_lang_by_date
'''
    insert_wikidata_by_lang_by_article
'''
def insert_wikidata_by_lang_by_article(lang, article):
    _, qid = get_qid(lang, article)
    print(f'qid {qid}')

    wikidata_stuff = {}

    if qid == f"Q_{lang}_" + article:
        #Redir
        wikidata_stuff = { 'label_en': '', 
                          'main_properties' : {}, 
                          'sitelinks' : {} 
    }
    else:
        wikidata_stuff = get_wikidata_stuff(lang, qid)
        
    insert_wikidata_stuff(lang, qid, article, wikidata_stuff)



insert_wikidata_by_lang_by_article('fr', 'Cédric_Doumbé')



