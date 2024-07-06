import sqlite3
import time
import requests
import json
WIKIDATA_TABLE = '_wikidata'
DB_NAME = './StatsWiki00.db'
SUPPORTED_YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
SUPPORTED_LANGUAGES = ['ar', 'az', 'de', 'en', 'eo', 'es', 'fr', 'ja', 'he', 'hy', 'it', 'ko', 'nl', 'pl', 'pt', 'ru', 'uk', 'zh']

'''
    SUPPORTED_REDIRECTS_BY_LANG
'''
SUPPORTED_REDIRECTS_BY_LANG = { 
    'ar': 
        {
            'قائمة الدول_والتبعيات حسب_عد السكان' : 'Q712280',
            'محمد بن سلمان بن عبد العزيز آل سعود' : 'Q6892571',
            'حوثيون' : 'Q3042087',
            'فيس بوك' : 'Q355'
        },
    'de': 
        {

        },
    'en': 
        {
            '2019–20coronavirus pandemic' : 'Q81068910',
            'Animal (2023 film)' : 'Q115947372',
            'Shōgun (2024 TV series)' : 'Q56276181',
            'Islamic State of Iraq and the Levant' : 'Q2429253',
            'List of Bollywood films of 2015' : 'Q17069681',
            'Ddd' : 'Q232923',
            'Straight Outta Compton (2015 film)' : 'Q18154625',
            'Suicide Squad (film)' : 'Q18604504',
            'United States presidential election, 2016' : 'Q699872',
            'List of Presidents of the United States' : 'Q35073',
            'AMGTV' : 'Q5380468',
            'List of Bollywood films of 2016' : 'Q19882412',
            'Stranger Things (TV series)' : 'Q19798734',
            'Meghan Markle' : 'Q3304418',
            'List of Bollywood films of 2017' : 'Q25999140',
            'Riverdale (2017 TV series)' : 'Q23001951',
            

        }, 
    'eo': 
        {
            'Kreo' : 'Q215304',
            'Romiaj ciferoj': 'Q38918',
            'Carolus Linnaeus': 'Q1043'
        },
    'es': 
        {

        },
    'fr': 
        {
            "Pandémie de maladie à coronavirus de 2019-2020" : "Q81068910",
            "Pandémie de maladie à coronavirus de 2020 en France" : "Q83873593",
            "Grippe de 1918" : "Q178275",
            "Charles de Galles" : "Q43274",
            "Mort de George Floyd" : "Q95579249",
            "Cédric Doumbé" : "Q24452252",
            "Coupe d'Afrique des Nations" : "Q83145"
        },
    'ja': 
        {
            '令和6年能登半島地震' : 'Q124060919'
        },
    'he': 
        {
            'ערים בישראל' : 'Q28330'
        },
    'hy': 
        {

        },
    'it': 
        {

        },
    'ko': 
        {
            '지구 온난화' : "Q7942"
        },
    'nl': 
        {
            'Google Inc.' : "Q95",
            'Saga o wiedźminie' : 'Q11835640'
        },
    'pl': 
        {
            'Mariusz Kamiński (minister)' : 'Q3845166'
        },
    'pt': 
        {

        },
    'ru': 
        {
            "Смерть Алексея Навального" : 'Q124556504',
            "Надеждин, Борис Борисович (политик)" : 'Q4311880'
        },
    'uk': 
        {
            'Російське вторгнення в Україну (2022)' : 'Q110999040',
            'Радіо «Свобода»' : 'Q485500'
        },
    'zh': 
        {

        }
}

FILTERS_BY_LANG = {
    'global' :
        (
            'MediaWiki:', 
            '????:', 
            'Portal:', 
            'File:', 
            'Help:', 
            'Category:', 
            'Main_Page', 
            '�', 
            'User:', 
            'Template:', 
            'Special:', 
            'Wikipedia:',  
            'Catégorie:', 
            'Spécial:', 
            'Wikipédia', 
            'Project:',
            '404.php',
            'xss',
            'Orangemorange',
            'Wiki',
        ),
    'ar' :
        (
            'تصنيف:', 
            'خاص:', 
            'ويكيبيديا:', 
            'ويكيبيديا:',
            'الصفحة_الرئيسية',
            'ملف:',
        ),
    'de' : 
        (  
            'Kategorie:', 
            'Hauptseite', 
            'Spezial:', 
            'Benutzer:', 
            'Datei:',
            'Liste_der_größten_Auslegerbrücken',
        ),
    'en' : 
        (
            '.xxx',
        ),
    'eo' :
        (
            'Portalo:', 
            'Helpo:', 
            'Vikipedio:', 
            'Speciala', 
            'Uzanto:',
            'Kategorio:',
            'Vikipedia_diskuto:',
            'Ŝablono:',
            'XXX',
            'Uzanto-Diskuto:',
        ),    
    'es' : 
        (
            'Especial:',
            'Archivo:',
            'Cleopatra_I_de_Egipto',
        ),
    'fr' : 
        (

            'Accueil', 
            'Wikip�', 
            'Sp?cial:', 
            'Fichier:', 
            'Aide:',
            'Cookie_(informatique)',
            'Utilisateur:',
            'Portail:',
        ),
    'he' : 
        (
            'משתמש:', 
            'קובץ:', 
            'עמוד_ראשי', 
            'מיוחד:', 
            'ויקיפדיה:',
        ),
    'hy' : 
        (
            'Կաղապար:', 
            'Վիքիպեդիա:', 
            'Կատեգորիա:', 
            'Գլխավոր_էջ', 
            'Ստորոգութիւն:', 
            'Սպասարկող:',
            'Վիքինախագիծ:',
            'Մասնակից:',
         ),
    'ko' : 
        (
            '특수:', 
            '최근_바뀜',
            '위키백과:', 
            '특수:',
            '폰허브',
            '분류:',
            '문화방송',
            '한국방송공사',
        ),    
    'it' :
        (
            'Pagina', 
            'Speciale:'
        ),
    'ja' :
        (
            'メインページ', 
            '特別:', 
            'Re:',
        ),
    'nl' : 
        (
            'Hoofdpagina', 
            'Speciaal:',
            'ChatGPT',
        ),
    'pl':
        (
            'Specjalna:', 
            'Strona_główna',
            'Szablon:',
            'Plik:',
        ),
    'pt' : 
        (
            'Usuário(a) Discussão:', 
            'Wikip�', 
            'Especial:', 
            'Ficheiro:', 
            'Predefinição:',
            'ChatGPT',
        ),
    'ru' :
        (
            'Категория:',
            'Википедия:',
            'Первый мститель:', 
            'Заглавная_страница', 
            'Служебная:',
            'Яндекс',
        ),
    'uk' : 
        (
            'Дюна:', 
            'Файл:', 
            'Спеціальна:', 
            'Вікіпедія:', 
            'Головна_сторінка',
        ),
    'zh' : 
        (
            '維基媒體基金會', 
            '首页',
        ),
    'az' : 
       (
           'Ana_Səhifə',
           'Xüsusi:',
           'Şəkil:'
       ),    

}

REDIRECTS_OUTPUT_FILE = "redirects.txt"

'''
    WIKIDATA_PROPERTIES
'''
WIKIDATA_PROPERTIES = {
    'direct' : {
        'P18':'image',
        'P402': 'relation OSM',
        'P10689': 'way OSM',
        'P11693': 'node OSM'
    },
    'non_direct' : {
        'P31':'instance of',
        'P21':'sex or gender',
        'P17':'country',
        'P131': 'administrative entity'
   }
   
}

'''
    insert_wikidata_stuff
'''
def insert_wikidata_stuff(lang, qid, article_, stuff):
    #print(stuff)
    table = WIKIDATA_TABLE
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print(qid)

    if not qid.startswith("Q_"):
        
        en_translation = stuff.get('label_en', '') or stuff.get('sitelinks', {}).get('en', '').replace('_', ' ')
        props = json.dumps(stuff.get('main_properties', {}))
        sitelinks = stuff.get('sitelinks', {})

        columns = ['qid', 'en_translation', 'props']
        values = [qid, en_translation, props]
        
        for langwiki, site in sitelinks.items():
            lang = langwiki.replace('wiki', '')
            if lang in SUPPORTED_LANGUAGES:
                column_name = f'{lang}_title'
                columns.append(column_name)
                value_name = site['title'].replace(" ", "_")
                values.append(value_name)

        columns_str = ', '.join(columns)
        placeholders = ', '.join(['?' for _ in range(len(columns))])

        insert_query = f'''
        REPLACE INTO {table} ({columns_str}) VALUES ({placeholders})
        '''
        
        try:
            cursor.execute(insert_query, values)
            conn.commit()   
        except sqlite3.Error as e:
            print(f"{e}")
        
    else: # SHADOW_QID

        insert_query = f"""
        INSERT INTO {table} (qid, {lang}_title) VALUES (?, ?);
        """

        try:
            #print(insert_query,  (qid, article_))
            cursor.execute(insert_query, (qid, article_))
            conn.commit()   
        except sqlite3.Error as e:
            print(f"{e}")

    conn.close()

'''
    get_qid
'''
def get_qid(lang, article):

    #print(f'article {article}')
    url = f'https://{lang}.wikipedia.org/w/api.php?action=query&titles={article}&prop=pageprops&format=json'

    headers = {'User-Agent': 'MyApp/1.0 (myemail@example.com)'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:

        pageid = ""
        wikidata = ""

        data = response.json()
        pages = data['query']['pages']
        for page in pages.values():
            #print(page)
            pageid = page.get('pageid', "")
            break
        
        if not pageid:
            return "", ""
        else:
            try:
                wikidata = pages[f'{pageid}']['pageprops']['wikibase_item']
                return pageid, wikidata
            except:
                wikidata = f"Q_{lang}_" + str(article)
                #with open(REDIRECTS_OUTPUT_FILE, 'a') as file:
                #    file.write(f"{lang}-{wikidata}: {article} \n")
                return pageid, wikidata
    

'''
    get_main_properties
'''
def get_main_properties(lang, claims, qid):

    dprops = WIKIDATA_PROPERTIES['direct']
    ndprops = WIKIDATA_PROPERTIES['non_direct']
    
    direct_props = list(set(dprops.keys()).intersection(claims.keys()))
    non_direct_props = list(set(ndprops.keys()).intersection(claims.keys()))

    results = {}

    for prop in direct_props:

        claim = claims[prop]
        
        # 'snaktype': 'datavalue': 'value':        
        claim_mainsnak = list(claim[0].values())[0]
        claim_value = ""
        try:
            claim_value = str(claim_mainsnak['datavalue']['value'])
        except Exception as e:
            print(f"direct_prop ['datavalue']['value']: {lang}-{qid}")
        results[prop] = claim_value

    for prop in non_direct_props:

        claim = claims[prop]
        # [{'mainsnak': {'snaktype': 'novalue', 'property': 'P17', 'hash': '9bd0d5bb5273ae454d4fbf369b5913462e400339', 'datatype': 'wikibase-item'}, 'type': 'statement', 'id': 'Q46$aede7db1-4cf4-163a-a357-a991a592a336', 'rank': 'normal'}]
        condition = claim[0]['mainsnak']['snaktype']
        if condition == 'value':
            claim_value = claim[0]['mainsnak']['datavalue']['value']['id']
            results[prop] = claim_value
        else:
            results[prop] = ''


    return json.dumps(results)


'''
    get_wikidata_stuff
'''
def get_wikidata_stuff(lang, qid):

    base_url = 'https://www.wikidata.org/w/api.php'

    # label_en
    response = requests.get(url=base_url, params={
        'action': 'wbgetentities',
        'ids': qid,  
        'languages': 'en',  
        'props': 'labels',
        'format': 'json'
    })
    data = response.json()
    label_en = ''
    try:
        first = data['entities'][qid]['labels'].get('en', {})
        if first:
            label_en = first['value']
    except:
        with open(REDIRECTS_OUTPUT_FILE, 'a') as file:
            file.write(f"{lang}-{qid}\n")
    # label_en ok


    # props, images
    response = requests.get(url=base_url, params={
        'action': 'wbgetentities',
        'ids': qid,
        'languages': lang,
        'props': 'claims',
        'format': 'json'
    })
    data = response.json()
    main_properties = None
    try:
        claims = data['entities'][qid]['claims']
        main_properties = get_main_properties(lang, claims, qid)
    except:
        with open(REDIRECTS_OUTPUT_FILE, 'a') as file:
            file.write(f"{lang}-{qid}\n")
    # props, images ok

    # Les interwikis
    response = requests.get(url=base_url, params={
        'action': 'wbgetentities',
        'ids': qid,
        'props': 'sitelinks',
        'format': 'json'
    })
    data = response.json()
    sitelinks = None
    try:
        sitelinks = data['entities'][qid]['sitelinks']
    except:
        with open(REDIRECTS_OUTPUT_FILE, 'a') as file:
            file.write(f"{lang}-{qid}\n")
    
    return {
        'label_en': label_en,
        'main_properties': main_properties,
        'sitelinks': sitelinks
    }

'''
    filter_results
'''
def filter_results(lang, article):

    filters = tuple(FILTERS_BY_LANG[lang]) + tuple(FILTERS_BY_LANG['global'])
    for filter in filters:
        if article.startswith(filter):
            return False
    return True


'''
    insert_wikidata_by_lang_by_article
'''
def insert_wikidata_by_lang_by_article(lang, article_tuple):
    article = article_tuple[0]
    _, qid = get_qid(lang, article)

    #if article in SUPPORTED_REDIRECTS_BY_LANG[lang].keys():
    #    return

    if filter_results(lang, article):
        wikidata_stuff = {}
        if qid == f"Q_{lang}_" + article:
            #Redir
            wikidata_stuff = { 'label_en': '', 
                            'main_properties' : {}, 
                            'sitelinks' : {} 
        }
        else:
            wikidata_stuff = get_wikidata_stuff(lang, qid)
        print(f'{qid} {article} {lang}')
        insert_wikidata_stuff(lang, qid, article, wikidata_stuff)

################################

print("*** azero, bitch")
sql_query = "SELECT article from az_2015 ORDER BY views DESC LIMIT 200"
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
results = cursor.execute(sql_query)
articles = results.fetchall()
conn.close()

for article in articles:
    time.sleep(0.15)
    try:
        insert_wikidata_by_lang_by_article('az', article)
    except:
        print("bitch, azero")


