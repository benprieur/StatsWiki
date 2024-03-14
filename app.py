from flask import Flask,render_template
from const.constants import SUPPORTED_LANGUAGES, SUPPORTED_YEARS
from const.constants_langs import FLAGS_STUFF, GlOBAL_PAGE_STUFF
from apps.app_year import by_year_lang
from apps.app_month import by_month_lang
from apps.app_day import by_day_lang
from apps.app_lang import by_lang
import random

app = Flask(__name__)

'''
    index
'''
@app.route("/")
def index():

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
def app_by_lang(lang):
    return by_lang(lang)

    
    




'''
    by_day_lang
'''
@app.route('/<lang>/<int:year>/<int:month>/<int:day>/', strict_slashes=False)
def app_by_day_lang(lang, year, month, day):
    return by_day_lang(lang, year, month, day)
                            

'''
    by_month_lang
'''
@app.route('/<lang>/<int:year>/<int:month>/', strict_slashes=False)
def app_by_month_lang(lang, year, month):
    return by_month_lang(lang, year, month)

    
'''
    by_year_lang
'''
@app.route('/<lang>/<year>', strict_slashes=False)
def app_by_year_lang(lang, year):
    return by_year_lang(lang, year)
    

if __name__ == '__main__':
    app.run(debug=True)

# FLASK_APP=app.py FLASK_DEBUG=1 flask run
# stat
