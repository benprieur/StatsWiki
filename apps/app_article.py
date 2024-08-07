from flask import Flask,render_template, jsonify
from const.constants import SUPPORTED_LANGUAGES
from const.constants_langs import FLAGS_STUFF
from db.dbRequestLayer import request_by_lang_by_qid


'''
    by_article
'''
def by_article(lang, qid, api=False):
    
    response = request_by_lang_by_qid(lang, qid)
    if not response:
        return {}
    
    return jsonify({
        "lang" : lang,
        "qid" : qid,
        "title" : response['title'],
        'en_translation' : response['en_translation'],
        'sentence' : response['sentence'],
        "wikidata_image" : response['wikidata_image'],
        "wikidata_image_url" : response['wikidata_image_url'],
        'statistics_global' : response['statistics_global']
    })

