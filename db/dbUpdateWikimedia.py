from datetime import datetime, timedelta
from dbInsertLayer import insert_by_day_by_lang
from wikimedia import request_from_wikimedia
from const.constants import SUPPORTED_LANGUAGES
from datetime import date
  
'''
    get_data_lang_start_end_date
'''
def get_data_lang_start_end_date(lang, 
                                 start_year, 
                                 start_month, 
                                 start_day, 
                                 end_year, 
                                 end_month, 
                                 end_day):
    
    start_date = datetime(start_year, start_month, start_day)
    end_date = datetime(end_year, end_month, end_day)
    current_date = start_date

    while current_date <= end_date:
        results = request_from_wikimedia(lang,
                                         current_date.year, 
                                         current_date.month, 
                                         current_date.day)
        
        # Ici traiter la réponse avec des classes
        if results:        
            if len(results):
                print(f'Daily import for {lang}')
                insert_by_day_by_lang(lang, current_date.year, current_date.month, current_date.day, results)
        current_date += timedelta(days=1)


'''
    daily_update
'''
def daily_update():
    yesterday = date.today() - timedelta(days=1)
    for lang in SUPPORTED_LANGUAGES:
        print(f'{lang}')
        get_data_lang_start_end_date(lang, yesterday.year, yesterday.month, yesterday.day, yesterday.year, yesterday.month, yesterday.day)

daily_update()