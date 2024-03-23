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

    if year not in SUPPORTED_YEARS:
        return Lines(lang)
    if lang not in SUPPORTED_LANGUAGES:
        return Lines(lang)
    
    lines = request_by_lang_by_date(lang, year)
    lines = display(lang, lines, year)
    
    previous_year = int(year) - 1
    next_year = int(year) + 1
    year_before, year_after = '', ''
    year_before_link = f'/{lang}/{previous_year:02d}'
    year_after_link = f'/{lang}/{next_year:02d}'
    year_before = str(previous_year)
    year_after = str(next_year)

    if not api:

        return render_template('year.html', 
        lang=lang,            
        articles=lines, 
        flag=FLAGS_STUFF[lang],
        year=str(year), 
        year_before_link=year_before_link,
        year_after_link=year_after_link,
        year_before=year_before,
        year_after=year_after,
        title=GlOBAL_PAGE_STUFF[lang]['title'] + ' ' + str(year),
        title_views=GlOBAL_PAGE_STUFF[lang]['title_views'], 
        title_article=GlOBAL_PAGE_STUFF[lang]['title_article'], 
        bymonthyear=YEAR_PAGE_STUFF[lang]['bymonthyear']
        )
    else:
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

