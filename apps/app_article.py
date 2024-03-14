from flask import render_template, redirect
from const.constants import SUPPORTED_LANGUAGES
from const.constants_langs import FLAGS_STUFF
from db.dbRequestLayer import request_by_lang_by_qid


'''
    by_article
'''
def by_article(lang, qid):
    
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
