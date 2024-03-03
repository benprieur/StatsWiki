from datetime import date
import requests
import time

def request_from_wikimedia(lang, year, month, day):
    date_ = date(year=year, month=month, day=day)
    date_str = date_.strftime('%Y/%m/%d')
    url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{lang}.wikipedia/all-access/{date_str}'

    try:
        headers = {'User-Agent': 'MyApp/1.0 (myemail@example.com)'}
        response = requests.get(url, headers=headers)
        time.sleep(0.15)
        if response.status_code == 200:
            data = response.json()
            top_articles = data['items'][0]['articles']
            return top_articles
    except requests.RequestException as e:
        print(f"{e}") 
        return None   
