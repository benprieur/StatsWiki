from flask import Flask,render_template, redirect, url_for, Response, request
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import json
import sqlite3
from datetime import date
from datetime import timedelta

from constants import SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF, MONTHS_BY_LANG, MONTH_PAGE_STUFF, YEAR_PAGE_STUFF, FILTERS_BY_LANG, SUPPORTED_REDIRECTS_BY_LANG
from constants_wikidata import FILTERERED_QIDS
from commons import get_commons_image_url

from dbRequestLayer import request_by_lang_by_articles_by_date, request_by_qid, request_by_lang_by_date, request_by_lang, request_dataviz, request_by_lang_by_qids_by_date, special_request_redirects
from wikimedia import get_first_sentence_wikipedia_article


app = Flask(__name__)

'''
    check_date
'''
def check_date(year, month=1, day=1):

    dt = date(year=year, month=month, day=day)
    today = date.today()
    yesterday = today - timedelta(days = 1)
    start_2015 = date(2015,7, 1)

    if dt <= yesterday and dt >= start_2015:
        return True
    return False

'''
    display
'''
def display(lang, articles, year=0, month=0, day=0):
    articles_display = create_display_dataset(lang, 
                                              articles, 
                                              year, 
                                              month, day)           
    articles_display = update_display_package_by_redirect(lang, 
                                                          articles_display, 
                                                          year, 
                                                          month, 
                                                          day)

    for _, props in articles_display.items():
        
        qid = props.get('qid', "")

        if qid in SUPPORTED_REDIRECTS_BY_LANG[lang].values():
            redirects_dict = props.get('redirects', {})
            if redirects_dict:
                global_sum = props.get('views', 0)

                for _views in redirects_dict.values():
                    views_value = 0
                    try:
                        views_value = int(_views)
                    except:   
                        views_value = 0

                    global_sum = global_sum + views_value

                props['total_views'] = global_sum
        else:    
            props['total_views'] = props['views']


    articles_display = dict(sorted(articles_display.items(), key=lambda item: item[1]['total_views'], reverse=True))
    return articles_display


'''
    update_display_package_by_redirect
'''
def update_display_package_by_redirect(lang, 
                                       articles_display,
                                       year,
                                       month,
                                       day):

    articles_to_remove = []
    articles_to_add = []

    for key, value in articles_display.items():
        article_ = key
        views = value['views']
        qid = value['qid']

        if qid in SUPPORTED_REDIRECTS_BY_LANG[lang].values():

            # Ici on a un article qui est dans le support redirect
            # L'article courant article_ est une redir
            articles_to_remove.append(article_)

            # On va chercher les infos relatives au main article
            main_article = request_by_lang_by_qids_by_date(lang, [qid], year, month, day)
            main_article = main_article[0]
            main_article_ = main_article[1]

            article_display = {}

            article_display['cleaned_article'] = main_article_.replace("_", " ")
            article_display['translation'] = main_article[2].replace("_", " ")
            article_display['wikidata_image_url'] = ''
            article_display['wikidata_image'] = ''
            article_display['qid'] = main_article[0]
            article_display['redirects'] = {}
            article_display['views'] = main_article[4]
            article_display['total_views'] = 0
            articles_to_add.append(article_display)

    # remove redirects
    for article_ in articles_to_remove:
        if article_ in articles_display.keys():
            articles_display.pop(article_)  

    # add target redirects
    for article_display in articles_to_add:
        key = article_display['cleaned_article'].replace(" ", "_")
        if key not in articles_display:
            articles_display[key] = article_display

    # Ici on parcourt toutes les lignes du dataset
    for article_, props in articles_display.items():
    
        qid = props.get('qid', {})
        redirects = []
        for key, val in SUPPORTED_REDIRECTS_BY_LANG[lang].items():
            if val == qid:
                redirects.append(key)
                
        views_redirects = special_request_redirects(lang,
                                            redirects,
                                            year,
                                            month,
                                            day)
        print(views_redirects)
        if views_redirects:
            for index, vr in enumerate(views_redirects[0]):
                views = 0
                try:
                    views = int(vr)
                except Exception as e:
                    print(f'{e} line 125 {vr}')
                
                props['redirects'][redirects[index]] = views

    return articles_display


'''
    get_value_from_string_by_key
'''
def get_value_from_string_by_key(str_analyze, key):
    # "\"{\\\"P18\\\": \\\"Dark vignette Al-Masjid AL-Nabawi Door800x600x300.jpg\\\", \\\"P21\\\": \\\"Q6581097\\\", \\\"P31\\\": \\\"Q5\\\"}\"" 
 
    start_index = str_analyze.find(key)
    start_value = str_analyze.find(":", start_index)
    start_delim = str_analyze.find("\"", start_value)
    end_delim = str_analyze.find("\"", start_delim+1)
    result = str_analyze[start_delim+1:end_delim]
    result = result.replace ("\\", "")

    return result
    

'''
    create_display_dataset
'''
def create_display_dataset(lang, articles, year=0, month=0, day=0):

    response = articles
    if year != 0:
        response = request_by_lang_by_articles_by_date(lang, 
                                                   [article[1] for article in articles],
                                                   year,
                                                   month,
                                                   day)
    '''
    qid,
    {lang}_title,
    en_translation,
    props,
    views
    '''
    
    dict_articles = {}
    for line in response:
        qid = line[0]
        article = line[1]
        translation = line[2]
        props = line[3]
        views = line[4]

        props_str = json.dumps(props)
        wikidata_image, wikidata_image_url = '', ''
        if props_str != 'null':
            wikidata_image = get_value_from_string_by_key(props_str, "P18")
            wikidata_image_url =  ""
            if wikidata_image:
                wikidata_image_url = 'https://commons.wikimedia.org/wiki/File:' + wikidata_image.replace(' ', '_')
                wikidata_image = get_commons_image_url(wikidata_image_url)

        if article not in FILTERERED_QIDS.values():
            article_display = {}
            article_display['cleaned_article'] = article.replace("_", " ")
            article_display['views'] = views
            article_display['translation'] = translation.replace("_", " ")
            article_display['wikidata_image_url'] = wikidata_image_url
            article_display['wikidata_image'] = wikidata_image
            article_display['qid'] = qid
            article_display['redirects'] = {}
            article_display['total_views'] = 0
            dict_articles[article] = article_display

    return dict_articles


'''
    check_results
'''
def check_results(results):

    try:
        if results is None:
            return False
        if results == []:
            return False
        else:
            return True
    except Exception as e:
        print(f'{e} check_results line 224')    
        return False
    

'''
    index
'''
@app.route("/")
def index():
    return render_template('index.html', 
        flags=FLAGS_STUFF,                   
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
        
        articles_display = display(lang, articles)

        return render_template('index_lang.html', 
                lang=lang,
                langs=SUPPORTED_LANGUAGES,
                flag=FLAGS_STUFF[lang],
                flags=FLAGS_STUFF,  
                title = GlOBAL_PAGE_STUFF[lang]['title'],
                titles={lang: info['title'] for lang, info in GlOBAL_PAGE_STUFF.items()},
                years = SUPPORTED_YEARS,
                articles=articles_display
        )
    
    elif lang == 'ads.txt':
            return 'google.com, pub-2569045443543971, DIRECT, f08c47fec0942fa0'
    
    else:
        return redirect("/", code=302)


'''
    by_day_lang
'''
@app.route('/<lang>/<int:year>/<int:month>/<int:day>/', strict_slashes=False)
def by_day_lang(lang, year, month, day):

    if not check_date(year, month, day):
        return redirect("/", code=302)
    
    if lang in SUPPORTED_LANGUAGES and int(year) in SUPPORTED_YEARS:
        articles = request_by_lang_by_date(lang, year, month, day)
        if not check_results(articles):
            return redirect("/", code=302)

        articles_display = display(lang, 
                                   articles, 
                                   year, 
                                   month, 
                                   day)
         
        day_current = date(year=year, month=month, day=day)
        day_before_date = day_current - timedelta(days=1)
        day_after_date = day_current + timedelta(days=1)
        day_before_link = f'/{lang}/{day_before_date.year}/{day_before_date.month:02d}/{day_before_date.day:02d}'
        day_after_link = f'/{lang}/{day_after_date.year}/{day_after_date.month:02d}/{day_after_date.day:02d}'
        day_after_str, day_before_str = '', ''
        if check_results(request_by_lang_by_date(lang, 
                                                day_before_date.year, 
                                                day_before_date.month, 
                                                day_before_date.day)):
            day_before_str = f'<< {day_before_date.year}/{day_before_date.month:02d}/{day_before_date.day:02d}'
        if check_results(request_by_lang_by_date(lang, 
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
                langs = SUPPORTED_LANGUAGES,
                year=f'{year}',
                flags=FLAGS_STUFF,
                flag=FLAGS_STUFF[lang],
                current_month_link=current_month_link
        )
                            

'''
    by_month_lang
'''
@app.route('/<lang>/<int:year>/<int:month>/', strict_slashes=False)
def by_month_lang(lang, year, month):
    
    if not check_date(year, month):
        return redirect("/", code=302)
    
    if lang in SUPPORTED_LANGUAGES and year in SUPPORTED_YEARS:
        articles = request_by_lang_by_date(lang, year, month)

        if not check_results(articles):
            return redirect("/", code=302)

        articles_display = display(lang, 
                                   articles,
                                    year, 
                                    month)
         
        month_current_date = date(year=year, month=month, day=15)
        month_before_date = month_current_date - relativedelta(days=30)
        month_after_date = month_current_date + relativedelta(days=30)
        month_before_link = f'/{lang}/{month_before_date.year}/{month_before_date.month:02d}'
        month_after_link = f'/{lang}/{month_after_date.year}/{month_after_date.month:02d}'
        current_month = MONTHS_BY_LANG[lang][month-1]

        month_before, month_after = '', ''
        if check_results(request_by_lang_by_date(lang, 
                                                  month_before_date.year, 
                                                  month_before_date.month,
                                                  )): 
            month_before = '<< ' + MONTHS_BY_LANG[lang][month_before_date.month-1] + ' ' + str(month_before_date.year)
        if check_results(request_by_lang_by_date(lang, 
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
                flags=FLAGS_STUFF[lang],                      
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
    
    if not check_date(year):
        return redirect("/", code=302)
    
    if lang in SUPPORTED_LANGUAGES and year in SUPPORTED_YEARS:
        articles = request_by_lang_by_date(lang, year)

        if not check_results(articles):
            return redirect("/", code=302)

        articles_display = display(lang, 
                                   articles, 
                                   year)
        
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
        if check_results(request_by_lang_by_date(lang, previous_year)):
            year_before = '<< ' + str(previous_year)
        if check_results(request_by_lang_by_date(lang, next_year)):
            year_after = str(next_year) + ' >>'

        return render_template('year.html', 
                lang=lang,            
                articles=articles_display, 
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
    else:
        return redirect("/", code=302)


'''
    byArticle
'''
@app.route("/<lang>/<qid>", strict_slashes=False)
def by_article(lang, qid):
    if not qid.startswith('Q'):
        return redirect("/", code=302)
    
    if lang not in  SUPPORTED_LANGUAGES:
        return redirect("/", code=302)
    
    response = request_dataviz(lang, qid)
    print(response)
    try:
        article = response[0]
        title = article[1]
        translation = article[2]
        props_str = json.dumps(article[3])
        months = []
        data = response[0][4:]
        months = [month for _ in SUPPORTED_YEARS for month in range(1,13)]
        statistics = []
        for index, month in enumerate(months):
            if index > 6 and index < 114:
                statistics.append((month, data[index]))

        wikidata_image, wikidata_image_url = '', ''
        if props_str != 'null': #JSON stuff, to rewrite
            wikidata_image = get_value_from_string_by_key(props_str, "P18")
            wikidata_image_url =  ""
            if wikidata_image:
                wikidata_image_url = 'https://commons.wikimedia.org/wiki/File:' + wikidata_image.replace(' ', '_')
                wikidata_image = get_commons_image_url(wikidata_image_url)

        sentence = get_first_sentence_wikipedia_article(lang, title)
        if '.' not in sentence:
            words = sentence.split()
            if len(words) > 20:
                sentence = ' '.join(words[:20])
    except:
        return redirect("/", code=302)

    return render_template('article.html', 
                lang=lang,
                qid=qid,            
                title=title,
                wikidata_image=wikidata_image,
                wikidata_image_url=wikidata_image_url,
                flag = FLAGS_STUFF[lang],
                sentence = sentence,
                translation=translation,
                statistics = statistics
    )
    

if __name__ == '__main__':
    app.run(debug=True)

# FLASK_APP=app.py FLASK_DEBUG=1 flask run
# stat
