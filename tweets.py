from datetime import datetime, timedelta
from datetime import date

import tweepy
import time

from dbRequestLayer import request_by_lang_by_date
from constants import SUPPORTED_LANGUAGES
from constants_langs import DAILY_TWEET_SENTENCE
from constants_wikidata import FILTERERED_QIDS

'''
    daily_tweet
'''
def daily_tweet():
    yesterday = date.today() - timedelta(days=1)
    for lang in SUPPORTED_LANGUAGES:
        
        articles = request_by_lang_by_date(lang,
                                          yesterday.year,
                                          yesterday.month,
                                          yesterday.day
                                         )

        articles_display = []
        for article in articles:
            qid = article[0]
            
            if qid not in FILTERERED_QIDS.keys():
                article_ = article[1]
                cleaned_article = article_.replace("_", " ")
                views = article[4]
                translation = article[2]
                articles_display.append([ 
                                         cleaned_article, 
                                         views
                                        ])
                 
        yesterday_str = yesterday.strftime('%Y/%m/%d')
        text = DAILY_TWEET_SENTENCE[lang] +  ' '+ f'({yesterday_str})\n'
        url = f'https://statswiki.info/{lang}/{yesterday.year}/{yesterday.month}/{yesterday.day}'
        for index in range(0, 3):
            match (index):
                case 0: text += "🥇 "
                case 1: text += "🥈 "
                case 2: text += "🥉 "
            text += f'{articles_display[index][0]}' 
            text += f' ({articles_display[index][1]})\n'
        text += f'{url}\r\n'
        print(text)
        tweet_upload_v2(text)


'''
    tweet_upload_v2
'''
def tweet_upload_v2(text):
    consumer_key = 'xwHjpvbGeguy63Za2y9V3bdGk'
    consumer_secret = 'rkHW5QJ5CjdL1Fm0RzEpOkc5qbetH84sOnJdCTxYzjP6mHSqv4'
    access_token = '1099344851982843904-wqUsm1YfPpNSAZ7SyOGTo5lDWvGuAU'
    access_token_secret = 'WxkOk8eJ1S8fZ7lATMpRJ8h4Ai67juGLXutxtmavbBdKG'

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    try:
        tweet = f"{text}"
        client.create_tweet(text=tweet)
        print("Tweeted:", tweet)
        time.sleep(5)
    except Exception as e: 
        print(e)
      
daily_tweet()