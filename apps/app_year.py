from apps.app_toolbox import display
from flask import render_template, jsonify
from const.constants import SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from const.constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF, MONTHS_BY_LANG, YEAR_PAGE_STUFF
from db.dbRequestLayer import request_by_lang_by_date

from flask import render_template, jsonify
from const.constants import SUPPORTED_LANGUAGES
from const.constants_langs import FLAGS_STUFF
from objects import Lines

'''
    by_year
'''     
def by_year(lang, year, api=False):
    
    lines = request_by_lang_by_date(lang, year)
    lines = display(lang, lines, year)
    
    return jsonify({
        'lang' : lang,            
        'year' : year, 
        'months' : MONTHS_BY_LANG[lang],
        'title' : GlOBAL_PAGE_STUFF[lang]['title'],
        'title_views' : GlOBAL_PAGE_STUFF[lang]['title_views'], 
        'title_article' : GlOBAL_PAGE_STUFF[lang]['title_article'], 
        'bymonthyear' : YEAR_PAGE_STUFF[lang]['bymonthyear'],
        'lines' : [item.to_dict() for item in lines.items]
    })

