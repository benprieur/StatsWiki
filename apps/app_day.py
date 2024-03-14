from apps.app_toolbox import display
from flask import render_template, redirect
from const.constants import SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from const.constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF, MONTH_PAGE_STUFF, MONTHS_BY_LANG
from db.dbRequestLayer import request_by_lang_by_date
from datetime import date, timedelta

'''
    by_day_lang
'''
def by_day_lang(lang, year, month, day):

    if lang in SUPPORTED_LANGUAGES and year in SUPPORTED_YEARS:
        
        lines = request_by_lang_by_date(lang, year, month, day)   
        lines = display(lang, lines, year, month, day)
         
        day_current = date(year=year, month=month, day=day)
        day_before_date = day_current - timedelta(days=1)
        day_after_date = day_current + timedelta(days=1)
        day_before_link = f'/{lang}/{day_before_date.year}/{day_before_date.month:02d}/{day_before_date.day:02d}'
        day_after_link = f'/{lang}/{day_after_date.year}/{day_after_date.month:02d}/{day_after_date.day:02d}'
        day_after_str, day_before_str = '', ''
        day_before_str = f'<< {day_before_date.year}/{day_before_date.month:02d}/{day_before_date.day:02d}'
        day_after_str = f'{day_after_date.year}/{day_after_date.month:02d}/{day_after_date.day:02d} >>'

        current_month_link = f'/{lang}/{day_current.year}/{day_current.month}'
        current_month = MONTHS_BY_LANG[lang][month-1]

        return render_template('day.html', 
                articles=lines, 
                current_date=f'{year}/{month:02d}/{day:02d}', 
                day= f'{day:02d}',
                day_after=day_after_str,
                day_before=day_before_str, 
                day_after_link=day_after_link,
                day_before_link=day_before_link,
                title=GlOBAL_PAGE_STUFF[lang]['title'],
                current_month=current_month,
                lang=lang,
                langs = SUPPORTED_LANGUAGES,
                year=f'{year}',
                flags=FLAGS_STUFF,
                flag=FLAGS_STUFF[lang],
                current_month_link=current_month_link
        )
    else:
        return redirect("/", code=302)