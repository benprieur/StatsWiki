from datetime import date
import requests
import time

def get_top_articles_from_wikipedia(yy, mm, dd, lang):
    date_ = date(year=yy, month=mm, day=dd)
    date_str = date_.strftime('%Y/%m/%d')
    print(f'{lang} : {date_str}')
    url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{lang}.wikipedia/all-access/{date_str}'

    try:
        headers = {'User-Agent': 'MyApp/1.0 (myemail@example.com)'}
        response = requests.get(url, headers=headers)
        time.sleep(0.09)
        if response.status_code == 200:
            data = response.json()
            top_articles = data['items'][0]['articles']
            return top_articles
    except requests.RequestException as e:
        print(f"{e}") 
        return None   

#get_top_articles_from_wikipedia(2024, 2, 23, 'fr')