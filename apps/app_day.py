from apps.app_toolbox import display
from flask import jsonify
from const.constants_langs import GlOBAL_PAGE_STUFF, MONTHS_BY_LANG
from db.dbRequestLayer import request_by_lang_by_date

'''
    by_day_lang
'''
def by_day(lang, year, month, day, api=False):

    lines = request_by_lang_by_date(lang, year, month, day)   
    lines = display(lang, lines, year, month, day)
    return jsonify({
        'lang' : lang,      
        'year' : year,
        'month' : month,
        'day' : day,
        'current_date' : f"{year}-{month:02d}-{day:02d}",
        'title' : GlOBAL_PAGE_STUFF[lang]['title'], 
        'lines' : [item.to_dict() for item in lines.items],
        'title_article' :GlOBAL_PAGE_STUFF[lang]['title_article'], 
        'title_views' :GlOBAL_PAGE_STUFF[lang]['title_views'],
        'localized_month': MONTHS_BY_LANG[lang][month-1]
    })
