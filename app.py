from flask import Flask,render_template
#from flask_cors import CORS
from const.constants import SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from const.constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF
from apps.app_year import by_year
from apps.app_month import by_month
from apps.app_day import by_day
from apps.app_lang import by_lang
from apps.app_article import by_article


app = Flask(__name__)
#CORS(app)

'''
    api_by_lang_by_article
'''
@app.route('/api/<lang>/<qid>/', strict_slashes=False)
def api_by_lang_by_article(lang, qid):
    print(f'api_by_article {lang} {qid}')
    return by_article(lang, qid, True)


'''
    api_by_year
'''
@app.route('/api/<lang>/<int:year>/', strict_slashes=False)
def api_by_year(lang, year):
    return by_year(lang, year, True)


'''
    api_by_month
'''
@app.route('/api/<lang>/<int:year>/<int:month>/', strict_slashes=False)
def api_by_month(lang, year, month):
    return by_month(lang, year, month, True)


'''
    api_by_day
'''
@app.route('/api/<lang>/<int:year>/<int:month>/<int:day>/', strict_slashes=False)
def api_by_day(lang, year, month, day):
    return by_day(lang, year, month, day, True)


'''
    api_by_lang
'''
@app.route('/api/<lang>', strict_slashes=False)
def api_by_lang(lang):
    print(f"api/{lang}")
    return "<html>API Lang</html>"

    
'''
    by_language
'''
@app.route("/<lang>", strict_slashes=False)
def app_by_lang(lang):
    return by_lang(lang)


@app.route('/', defaults={'path': ''}, strict_slashes=False)
@app.route('/<path:path>', strict_slashes=False)
def catch_all(path):
    if path.startswith('api'):
        return "API route not found", 404
    else:
        return "<html>Catch all</html>"


if __name__ == '__main__':
    app.run(debug=True)

# FLASK_APP=app.py FLASK_DEBUG=1 flask run
# stat
