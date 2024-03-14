from datetime import date
import requests
import time
import re

def request_from_wikimedia(lang, year, month, day):
    date_ = date(year=year, month=month, day=day)
    date_str = date_.strftime('%Y/%m/%d')
    url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{lang}.wikipedia/all-access/{date_str}'

    try:
        headers = {'User-Agent': 'MyApp/1.0 (myemail@example.com)'}
        response = requests.get(url, headers=headers)
        time.sleep(0.5)
        if response.status_code == 200:
            data = response.json()
            top_articles = data['items'][0]['articles']
            return top_articles
    except requests.RequestException as e:
        print(f"{e}") 
        return None   

'''
    get_first_sentence_wikipedia_article
'''
def get_first_sentence_wikipedia_article(lang, article_title):
    URL = f"https://{lang}.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": article_title,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
    }

    response = requests.get(URL, params=PARAMS)
    data = response.json()

    first_sentence = ""
    if data.get("query", {}):
        page = next(iter(data["query"]["pages"].values()))
        first_sentence = page["extract"][:120]
        first_sentence = re.sub( "[(),]", "", first_sentence)
        words = first_sentence.split(" ")
        first_sentence = ' '.join(words[:-1])
    return first_sentence