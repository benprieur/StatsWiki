from flask import Flask,render_template, redirect, url_for, Response
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import json
import sqlite3

from constants import SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF, MONTHS_BY_LANG, MONTH_PAGE_STUFF, YEAR_PAGE_STUFF, FILTERS_BY_LANG
from constants_wikidata import FILTERERED_QIDS

from dbRequestLayer import request_by_lang_by_year, request_by_lang_by_day, request_by_lang_by_month, request_by_lang, request_wikidata_stuff, request_wikidata_stuff_by_article

app = Flask(__name__)

'''
    check_results
'''
def check_results(results):
    try:
        ret = False
        if results is None:
            ret = False
        if results == []:
            ret = False
        elif results[0][1] == 0: 
            ret = False
        else:
            ret = True
        return ret
    except sqlite3.Error as e:
        print("CheckResults: sqlite3.Error")    
        return False
    except:
        print("CheckResults: General Error")   
        return False
    

'''
    index
'''
@app.route("/")
def index():
    return render_template('index.html', 
        imgs=FLAGS_STUFF,                   
        langs=SUPPORTED_LANGUAGES,
        years=SUPPORTED_YEARS,
        titles={lang: info['title'] for lang, info in GlOBAL_PAGE_STUFF.items()}
    )


'''
    by_language
'''
@app.route("/<lang>", strict_slashes=False)
def by_language(lang):
    if lang in SUPPORTED_LANGUAGES:

        articles = request_by_lang(lang)
        if not check_results(articles):
            return redirect("/", code=302)

        results_wikidata = request_wikidata_stuff(lang, [article[0] for article in articles])
        translation_dict = {tup[1]: tup[2] for tup in results_wikidata}
        authorization_dict = {tup[1]: tup[0] for tup in results_wikidata}
        articles_display = []

        for article in articles:
            article_ = article[0]
            qid = authorization_dict.get(article_, '')
            if qid not in FILTERERED_QIDS.keys():
                article_cleaned = article_.replace("_", " ")
                views = article[1]
                translation = translation_dict.get(article_, '')
                articles_display.append([article_, 
                                        article_cleaned, 
                                        views, 
                                        translation])
            
        return render_template('index_lang.html', 
                lang=lang,
                langs=SUPPORTED_LANGUAGES,
                img=FLAGS_STUFF[lang],
                imgs=FLAGS_STUFF,  
                title = GlOBAL_PAGE_STUFF[lang]['title'],
                titles={lang: info['title'] for lang, info in GlOBAL_PAGE_STUFF.items()},
                years = SUPPORTED_YEARS,
                articles=articles_display
        )
    elif lang == 'filtering_by_wiki.json':
        json_data = json.dumps(FILTERS_BY_LANG, indent=4, ensure_ascii=False)
        return Response(json_data, mimetype='application/json')
    elif lang == 'global_filtering_by_qids.json':
        json_data = json.dumps(FILTERERED_QIDS, indent=4, ensure_ascii=False)
        return Response(json_data, mimetype='application/json')
    elif lang == 'ads.txt':
            return 'google.com, pub-2569045443543971, DIRECT, f08c47fec0942fa0'
    else:
        return redirect("/", code=302)


'''
    by_day_lang
'''
@app.route('/<lang>/<int:year>/<int:month>/<int:day>/', strict_slashes=False)
def by_day_lang(lang, year, month, day):
    results = []
    if lang in SUPPORTED_LANGUAGES and int(year) in SUPPORTED_YEARS:
        articles = request_by_lang_by_day(lang, year, month, day)
        if not check_results(articles):
            return redirect("/", code=302)

        results_wikidata = request_wikidata_stuff(lang, [article[0] for article in articles])
        translation_dict = {tup[1]: tup[2] for tup in results_wikidata}
        authorization_dict = {tup[1]: tup[0] for tup in results_wikidata}
        articles_display = []

        for article in articles:
            article_ = article[0]
            qid = authorization_dict.get(article_, '')
            if qid not in FILTERERED_QIDS.keys():
                article_cleaned = article_.replace("_", " ")
                views = article[1]
                translation = translation_dict.get(article_, '')
                articles_display.append([article_, 
                                        article_cleaned, 
                                        views, 
                                        translation])


        day_current = date(year=year, month=month, day=day)
        day_before_date = day_current - timedelta(days=1)
        day_after_date = day_current + timedelta(days=1)
        day_before_link = f'/{lang}/{day_before_date.year}/{day_before_date.month:02d}/{day_before_date.day:02d}'
        day_after_link = f'/{lang}/{day_after_date.year}/{day_after_date.month:02d}/{day_after_date.day:02d}'
        day_after_str, day_before_str = '', ''
        if check_results(request_by_lang_by_day(lang, 
                                                day_before_date.year, 
                                                day_before_date.month, 
                                                day_before_date.day)):
            day_before_str = f'<< {day_before_date.year}/{day_before_date.month:02d}/{day_before_date.day:02d}'
        if check_results(request_by_lang_by_day(lang, 
                                                day_after_date.year, 
                                                day_after_date.month,day_after_date.day)):
            day_after_str = f'{day_after_date.year}/{day_after_date.month:02d}/{day_after_date.day:02d} >>'

        current_month_link = f'/{lang}/{day_current.year}/{day_current.month}'
        current_month = MONTHS_BY_LANG[lang][month-1]

        return render_template('day.html', 
                articles=articles_display, 
                current_date=f'{year}/{month:02d}/{day:02d}', 
                day= f'{day:02d}',
                day_after=day_after_str,
                day_before=day_before_str, 
                day_after_link=day_after_link,
                day_before_link=day_before_link,
                title=GlOBAL_PAGE_STUFF[lang]['title'],
                current_month=current_month,
                lang=lang,
                year=f'{year}',
                imgs=FLAGS_STUFF[lang],
                current_month_link=current_month_link
        )
                            

'''
    by_month_lang
'''
@app.route('/<lang>/<int:year>/<int:month>/', strict_slashes=False)
def by_month_lang(lang, year, month):
    if lang in SUPPORTED_LANGUAGES and year in SUPPORTED_YEARS:
        articles = request_by_lang_by_month(lang, year, month)

        if not check_results(articles):
            return redirect("/", code=302)

        results_wikidata = request_wikidata_stuff(lang, [article[0] for article in articles])
        translation_dict = {tup[1]: tup[2] for tup in results_wikidata}
        authorization_dict = {tup[1]: tup[0] for tup in results_wikidata}
        articles_display = []

        for article in articles:
            article_ = article[0]
            qid = authorization_dict.get(article_, '')
            if qid not in FILTERERED_QIDS.keys():
                article_cleaned = article_.replace("_", " ")
                views = article[1]
                translation = translation_dict.get(article_, '')
                articles_display.append([article_, 
                                        article_cleaned, 
                                        views, 
                                        translation])


        month_current_date = date(year=year, month=month, day=15)
        month_before_date = month_current_date - relativedelta(days=30)
        month_after_date = month_current_date + relativedelta(days=30)
        month_before_link = f'/{lang}/{month_before_date.year}/{month_before_date.month:02d}'
        month_after_link = f'/{lang}/{month_after_date.year}/{month_after_date.month:02d}'
        current_month = MONTHS_BY_LANG[lang][month-1]

        month_before, month_after = '', ''
        if check_results(request_by_lang_by_month(lang, 
                                                  month_before_date.year, 
                                                  month_before_date.month,
                                                  )): 
            month_before = '<< ' + MONTHS_BY_LANG[lang][month_before_date.month-1] + ' ' + str(month_before_date.year)
        if check_results(request_by_lang_by_month(lang, 
                                                  month_after_date.year, 
                                                  month_after_date.month
                                                  )): 
            month_after = MONTHS_BY_LANG[lang][month_after_date.month-1] + ' ' + str(month_after_date.year) + ' >>'        

        num_days = calendar.monthrange(month_current_date.year, month_current_date.month)
        list_days_str = [f'/{lang}/{month_current_date.year}/{month_current_date.month:02d}/{day:02d}' for day in range(1, num_days[1] + 1)]
        if (date.today().year == month_current_date.year) and (date.today().month == month_current_date.month):
            list_days_str = [f'/{lang}/{month_current_date.year}/{month_current_date.month:02d}/{day:02d}' for day in range(1, date.today().day)]

        return render_template('month.html',
                lang=lang,
                title=GlOBAL_PAGE_STUFF[lang]['title'], 
                year=year,
                imgs=FLAGS_STUFF[lang],                      
                articles=articles_display, 
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

    
    
'''
    by_year_lang
'''
@app.route('/<lang>/<int:year>', strict_slashes=False)
def by_year_lang(lang, year):
    if lang in SUPPORTED_LANGUAGES and year in SUPPORTED_YEARS:
        articles = request_by_lang_by_year(lang, year)
        
        if not check_results(articles):
            return redirect("/", code=302)

        results_wikidata = request_wikidata_stuff(lang, [article[0] for article in articles])
        translation_dict = {tup[1]: tup[2] for tup in results_wikidata}
        authorization_dict = {tup[1]: tup[0] for tup in results_wikidata}
        articles_display = []

        for article in articles:
            article_ = article[0]
            qid = authorization_dict.get(article_, '')
            if qid not in FILTERERED_QIDS.keys():
                article_cleaned = article_.replace("_", " ")
                views = article[1]
                translation = translation_dict.get(article_, '')
                articles_display.append([article_, 
                                        article_cleaned, 
                                        views, 
                                        translation])


        list_months = []
        list_months_link = [] 
        for index, _ in enumerate(MONTHS_BY_LANG[lang]):
            results = request_by_lang_by_month(lang, year, index+1)
            if results:
                if results[0][1] > 0:
                    list_months.append(MONTHS_BY_LANG[lang][index])    
                    list_months_link.append(f'/{lang}/{year}/{index+1}')
        months = {}
        for index, month in enumerate(list_months):
            months[month] = list_months_link[index]
        
        previous_year = int(year) - 1
        next_year = int(year) + 1
        year_before, year_after = '', ''
        year_before_link = f'/{lang}/{previous_year:02d}'
        year_after_link = f'/{lang}/{next_year:02d}'
        if check_results(request_by_lang_by_year(lang, previous_year)):
            year_before = '<< ' + str(previous_year)
        if check_results(request_by_lang_by_year(lang, next_year)):
            year_after = str(next_year) + ' >>'

        return render_template('year.html', 
                articles=articles_display, 
                imgs=FLAGS_STUFF[lang],
                year=str(year), 
                year_before_link=year_before_link,
                year_after_link=year_after_link,
                year_before=year_before,
                year_after=year_after,
                months=months,
                title=GlOBAL_PAGE_STUFF[lang]['title'] + ' ' + str(year),
                title_views=GlOBAL_PAGE_STUFF[lang]['title_views'], 
                title_article=GlOBAL_PAGE_STUFF[lang]['title_article'], 
                bymonthyear=YEAR_PAGE_STUFF[lang]['bymonthyear'],
                lang=lang
        )
    else:
        return redirect("/", code=302)


'''
    byArticle
'''
@app.route("/<lang>/<article>", strict_slashes=False)
def by_article(lang, article):
    if lang in SUPPORTED_LANGUAGES:
        article = request_wikidata_stuff_by_article(lang, article)
        return f"<html>{article}</html>"
    return f""    

    


if __name__ == '__main__':
    app.run(debug=True)

# FLASK_APP=app.py FLASK_DEBUG=1 flask run
# stat
