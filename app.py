from flask import Flask,render_template, redirect, url_for, Response, request
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import json
from datetime import date
from datetime import timedelta
import re

from constants import SUPPORTED_LANGUAGES, SUPPORTED_YEARS, REDIRECTS_OUTPUT_FILE
from constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF, MONTHS_BY_LANG, MONTH_PAGE_STUFF, YEAR_PAGE_STUFF, SUPPORTED_REDIRECTS_BY_LANG
from constants_wikidata import FILTERERED_QIDS, SHADOW_QID
from commons import get_commons_image_url

from dbRequestLayer import request_by_lang_by_articles_by_date, request_by_lang_by_date, request_by_lang, request_by_lang_by_qid, request_by_lang_by_qid_by_date, special_request_redirect, get_value_from_string_by_key, request_qid_from_wikidata_table


app = Flask(__name__)

'''
    check_date_true_access
'''
def check_date_true_access(year, month=0, day=0):

    today = date.today()
    yesterday = today - timedelta(days = 1)
    start_2015 = date(2015,7, 1)
    
    if day:
        dt = date(year=year, month=month, day=day)
        if dt > yesterday or dt < start_2015:
            return False
    elif month:
        dt = date(year=year, month=month, day=1)
        if dt > yesterday or dt < start_2015:
            return False
    else:
        if year > 2024 or year < 2015:
            return False
    return True


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

        # Gros hack de merde
        if not props:
            props = {}
            props['views'] = 43
            props['total_views'] = 43 
        else:
            if not props['views']:
                props['views'] = 42
            if not props['total_views']:
                props['total_views'] = 43

        # Est-ce que le qid est une des cibles des redirections supportées
        # Si oui on somme les views des redirections
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

    # Ici on parcourt toutes les lignes du dataset
    for article_, props in articles_display.items():
    
        qid = props.get('qid', {})
        redirects = []
        if qid:

            # Pour un qid donné on regarde les redirections qui pointent sur ce qid. Le but est d'ajouter cet info à ce qid.
            for key, val in SUPPORTED_REDIRECTS_BY_LANG[lang].items():
                if val == qid:
                    redirects.append(key)
            
            for redirect in redirects:

                response = special_request_redirect(lang,
                                                    redirect,
                                                    year,
                                                    month,
                                                    day)
                views = 0                
                if response:
                    try:
                        views = int(response[0][0])
                    except Exception as e:
                        print(f'{e}')
                
                props['redirects'][redirect] = views

    return articles_display


'''
    create_display_dataset
'''
def create_display_dataset(lang, articles, year=0, month=0, day=0):

    response = articles
    #response = request_by_lang_by_articles_by_date(lang, [article[1] for article in articles], year, month, day)
    '''
    qid,
    {lang}_title,
    en_translation,
    props,
    views
    '''
    articles_to_add = []
    articles_to_remove = []
    for line in response:

        '''
        list_article_dict = {
            'title' : title,
            'translation' : translation,
            'statistics' : statistics,
            'wikidata_image' : wikidata_image,
            'wikidata_image_url' : wikidata_image_url,
            'sentence' : sentence,
            'redirects' : redirects
        }
        '''

        qid_ = line[0]
        article_ = line[1]
        views_ = line[4]

        if not article_:
            # L'article est dans le classement mais à été suppr, Q96379955 en 'ar' p.e
            articles_to_remove.append(line)
        
        elif not views_:
            articles_to_remove.append(line)

        else:

            if not qid_:
                # y réfléchir
                articles_to_remove.append(line)

            else:
                motif_straight = r'^Q\d+$'
                IS_STRAIGHT_QID = re.match(motif_straight, qid_) #Q122345
                IS_SHADOW_QID = True if qid_.startswith(SHADOW_QID) else False

                if IS_STRAIGHT_QID or IS_SHADOW_QID: 

                    qid_article_main_redirect = SUPPORTED_REDIRECTS_BY_LANG[lang].get(article_.replace("_", " "), {})

                    if qid_article_main_redirect:
                            # article_ est dans SUPPORTED_REDIRECTS_BY_LANG
                            # C'est un redirect géré
                            articles_to_remove.append(line)

                            # On demande les données de l'article principal
                            main_article, main_article_ = (), ""
                            req = request_by_lang_by_qid_by_date(lang, qid_article_main_redirect, year, month, day)
                            if req:
                                main_article = req[0]
                                main_article_ = main_article[1]
                            else:
                                # On a pas de données sur l'article dans la table-ci
                                # On contruit la liste pour lui en demandant à _wikidata             
                                #[ qid, {lang}_title, en_translation, props, views]
                                req_seconde_chance = request_qid_from_wikidata_table(lang, qid_article_main_redirect)

                                if req_seconde_chance:
                                    # main_article est un p... de tuple à la c...
                                    main_article = req_seconde_chance[0]
                                    main_article_ = main_article[1]
                                    main_article_qid_ = main_article[0]
                                    main_article_translation_ = main_article[2]
                                    main_article_props_ = main_article[3]

                                    main_article = (main_article_qid_, 
                                                    main_article_,
                                                    main_article_translation_,
                                                    main_article_props_,
                                                    0) # On ajoute 0 view

                                    main_article_ = main_article[1]

                            if main_article:
                                # Es-ce que le main est déjà dans le dataset ?
                                line__article_dict = [article[1] for article in articles]
                                if main_article_ not in line__article_dict:
                                    articles_to_add.append(main_article)
                # End if IS_STRAIGHT_QID or IS_SHADOW_QID:
                else:
                    # On a un article qui existe avec un qid qui existe
                    print(f"Line 222, app.py {qid_} {article_}")

  

    for element in articles_to_remove:
        response.remove(element)


    for element in articles_to_add:
        response.append(element)


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

        if qid not in FILTERERED_QIDS.keys():
            article_display = {}
            article_display['cleaned_article'] = article.replace("_", " ")
            article_display['views'] = views
            article_display['translation'] = "" if translation is None else translation.replace("_", " ")
            
            
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

    #une_lang = random.choice([ 'de', 'en', 'es', 'fr', 'ja', 'it', 'ko', 'nl', 'pl', 'pt'])
    #une_qid = random.choice([ 'Q26876', 'Q33881', 'Q33881'])  
    return render_template('index.html',
                langs=SUPPORTED_LANGUAGES,
                years=SUPPORTED_YEARS, 
                flags = FLAGS_STUFF,
                titles = GlOBAL_PAGE_STUFF
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

    if not check_date_true_access(year, month, day):
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
    
    if not check_date_true_access(year, month):
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
    
    if not check_date_true_access(year):
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
    
    response = request_by_lang_by_qid(lang, qid)
    if response:
        return render_template('article.html', 
                    lang=lang,
                    qid=qid,        
                    title=response['title'],
                    wikidata_image=response['wikidata_image'],
                    wikidata_image_url=response['wikidata_image_url'],
                    flag = FLAGS_STUFF[lang],
                    sentence =response['sentence'],
                    translation=response['translation'],
                    statistics=response['statistics'],
                    redirects =response['redirects']
                )
    else:
        return redirect("/", code=302)

    

if __name__ == '__main__':
    app.run(debug=True)

# FLASK_APP=app.py FLASK_DEBUG=1 flask run
# stat
