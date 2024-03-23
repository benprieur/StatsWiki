from apps.app_toolbox import display
from flask import render_template, redirect, jsonify
from const.constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF, MONTH_PAGE_STUFF, MONTHS_BY_LANG
from db.dbRequestLayer import request_by_lang_by_date
from datetime import date
import calendar

'''
    by_month
'''     
def by_month(lang, year, month, api=False):
    
    lines = request_by_lang_by_date(lang, year, month)
    lines = display(lang, lines, year, month)
    
    month_current_date = date(year=year, month=month, day=15)
    num_days = calendar.monthrange(month_current_date.year, month_current_date.month)
    list_days_str = [f'/{lang}/{month_current_date.year}/{month_current_date.month:02d}/{day:02d}' for day in range(1, num_days[1] + 1)]
    if (date.today().year == month_current_date.year) and (date.today().month == month_current_date.month):
        list_days_str = [f'/{lang}/{month_current_date.year}/{month_current_date.month:02d}/{day:02d}' for day in range(1, date.today().day)]

    print(list_days_str)
    
    print(MONTHS_BY_LANG[lang][month])
    return jsonify({
        'lang' : lang,            
        'title' : GlOBAL_PAGE_STUFF[lang]['title'], 
        'lines' : [item.to_dict() for item in lines.items],
        'days' : list_days_str,
        'bymonthday' :MONTH_PAGE_STUFF[lang]['byday'],
        'title_article' :GlOBAL_PAGE_STUFF[lang]['title_article'], 
        'title_views' :GlOBAL_PAGE_STUFF[lang]['title_views'],
        'localized_month': MONTHS_BY_LANG[lang][month-1]
    })
