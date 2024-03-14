from apps.app_toolbox import display
from flask import render_template, redirect
from const.constants import SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from const.constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF, MONTH_PAGE_STUFF, MONTHS_BY_LANG
from db.dbRequestLayer import request_by_lang_by_date
from datetime import date
import calendar
from dateutil.relativedelta import relativedelta

'''
    by_month_lang
'''
def by_month_lang(lang, year, month):
    
    if lang in SUPPORTED_LANGUAGES and year in SUPPORTED_YEARS:
        
        lines = request_by_lang_by_date(lang, year, month)
        lines = display(lang, lines, year, month)
         
        month_current_date = date(year=year, month=month, day=15)
        month_before_date = month_current_date - relativedelta(days=30)
        month_after_date = month_current_date + relativedelta(days=30)
        month_before_link = f'/{lang}/{month_before_date.year}/{month_before_date.month:02d}'
        month_after_link = f'/{lang}/{month_after_date.year}/{month_after_date.month:02d}'
        current_month = MONTHS_BY_LANG[lang][month-1]


        month_before = '<< ' + MONTHS_BY_LANG[lang][month_before_date.month-1] + ' ' + str(month_before_date.year)
        month_after = MONTHS_BY_LANG[lang][month_after_date.month-1] + ' ' + str(month_after_date.year) + ' >>'        

        num_days = calendar.monthrange(month_current_date.year, month_current_date.month)
        list_days_str = [f'/{lang}/{month_current_date.year}/{month_current_date.month:02d}/{day:02d}' for day in range(1, num_days[1] + 1)]
        if (date.today().year == month_current_date.year) and (date.today().month == month_current_date.month):
            list_days_str = [f'/{lang}/{month_current_date.year}/{month_current_date.month:02d}/{day:02d}' for day in range(1, date.today().day)]

        return render_template('month.html',
                lang=lang,
                title=GlOBAL_PAGE_STUFF[lang]['title'], 
                year=year,
                flags=FLAGS_STUFF[lang],                      
                articles=lines, 
                current_month=current_month, 
                month_after=month_after, 
                month_before=month_before, 
                month_after_link=month_after_link, 
                month_before_link=month_before_link,          
                current_year=year, 
                list_days_str=list_days_str,
                byday=MONTH_PAGE_STUFF[lang]['byday'], 
                title_article=GlOBAL_PAGE_STUFF[lang]['title_article'], 
                title_views=GlOBAL_PAGE_STUFF[lang]['title_views'],
        )
    else:
        return redirect("/", code=302)