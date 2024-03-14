from apps.app_toolbox import display
from flask import render_template, redirect
from const.constants import SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from const.constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF
from db.dbRequestLayer import request_by_lang

'''
    by_lang
'''
def by_lang(lang):
    
    if lang == 'ads.txt':
        return 'google.com, pub-2569045443543971, DIRECT, f08c47fec0942fa0'

    elif not lang in SUPPORTED_LANGUAGES:
        return redirect("/", code=302)
    
    else:
        lines = request_by_lang(lang)
        lines = display(lang, lines)
   
        return render_template('index_lang.html',               
            lang=lang,
            langs=SUPPORTED_LANGUAGES,
            flag=FLAGS_STUFF[lang],
            flags=FLAGS_STUFF,  
            title = GlOBAL_PAGE_STUFF[lang]['title'],
            titles={lang: info['title'] for lang, info in GlOBAL_PAGE_STUFF.items()},
            years = SUPPORTED_YEARS,
            articles=lines
        )