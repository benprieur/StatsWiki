from apps.app_toolbox import display
from apps.app_article import by_article
from flask import render_template, redirect
from const.constants import SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from const.constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF, MONTHS_BY_LANG, YEAR_PAGE_STUFF
from db.dbRequestLayer import request_by_lang_by_date

'''
    by_year_lang
'''
def by_year_lang(lang, tag):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect("/", code=302)
    
    print(tag)
    year = 0
    try:
        year = int(tag)
    except:
        print("app_year: except int-cast (year), allright baby.")

    if year in SUPPORTED_YEARS:
        
        lines = request_by_lang_by_date(lang, year)
        lines = display(lang, lines, year)
        
        list_months = []
        list_months_link = [] 
        for month, _ in enumerate(MONTHS_BY_LANG[lang]):
            results = request_by_lang_by_date(lang, year, month+1)
            if results:
                list_months.append(MONTHS_BY_LANG[lang][month])    
                list_months_link.append(f'/{lang}/{year}/{month+1}')
        months = {}
        for index, month in enumerate(list_months):
            months[month] = list_months_link[index]
        
        previous_year = int(year) - 1
        next_year = int(year) + 1
        year_before, year_after = '', ''
        year_before_link = f'/{lang}/{previous_year:02d}'
        year_after_link = f'/{lang}/{next_year:02d}'
        year_before = '<< ' + str(previous_year)
        year_after = str(next_year) + ' >>'

        return render_template('year.html', 
                lang=lang,            
                articles=lines, 
                flag=FLAGS_STUFF[lang],
                year=str(year), 
                year_before_link=year_before_link,
                year_after_link=year_after_link,
                year_before=year_before,
                year_after=year_after,
                months=months,
                title=GlOBAL_PAGE_STUFF[lang]['title'] + ' ' + str(year),
                title_views=GlOBAL_PAGE_STUFF[lang]['title_views'], 
                title_article=GlOBAL_PAGE_STUFF[lang]['title_article'], 
                bymonthyear=YEAR_PAGE_STUFF[lang]['bymonthyear']
        )
    elif tag.startswith("Q"):
        qid = tag # I know...
        return by_article(lang, qid)
    else:
        return redirect("/", code=302)