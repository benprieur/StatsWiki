from flask import Flask,render_template, jsonify
from const.constants import SUPPORTED_LANGUAGES
from const.constants_langs import FLAGS_STUFF
from db.dbRequestLayer import request_by_lang_by_qid


'''
    by_search_article
'''
def by_search_article(key_search, api=False):
    
    # Ici on renvoie la liste d'auto-complétion
    return None