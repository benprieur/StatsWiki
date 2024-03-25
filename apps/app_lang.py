from apps.app_toolbox import display
from flask import render_template, jsonify
from const.constants import SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from const.constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF
from db.dbRequestLayer import request_by_lang

'''
    by_lang
'''
def by_lang(lang, api=False):
    
    lines = request_by_lang(lang)
    lines = display(lang, lines)

    return jsonify({
        'lang' : lang,      
        'title' : GlOBAL_PAGE_STUFF[lang]['title'], 
        'lines' : [item.to_dict() for item in lines.items],
        'title_article' :GlOBAL_PAGE_STUFF[lang]['title_article'], 
        'title_views' :GlOBAL_PAGE_STUFF[lang]['title_views'],
    })
