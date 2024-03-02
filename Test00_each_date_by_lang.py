from datetime import date, timedelta
import calendar
from DatabaseRequest import request_data_date_lang
from GlobalData import SUPPORTED_LANGUAGES, SUPPORTED_YEARS

'''
    test lambda
''' 
def test_lambda():
    print(request_data_date_lang('fr', 2024, '08', '19'))

'''
    test_each_date_by_lang
''' 
def test_each_date_by_lang():
    log_output = []  # Liste pour stocker les couples lang-date sans données

    for lang in SUPPORTED_LANGUAGES:
        print(lang)
        for year in SUPPORTED_YEARS:
            print(f'{lang}-{year}')    
            start_date = date(year, 1, 1)
            number_days_by_year =  365
            if calendar.isleap(year):
                number_days_by_year = 366

            days = [start_date + timedelta(days=i) for i in range(number_days_by_year)]
            for day in days:
                results = request_data_date_lang(lang, day.year, f'{day.month:02d}', f'{day.day:02d}')
                if results[0][1] == 0:
                    print(f"{lang} - {day.year}-{day.month:02d}-{day.day:02d}")


if __name__ == '__main__':
    test_each_date_by_lang()