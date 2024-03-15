from datetime import timedelta
from datetime import date

import tweepy
import time

from db.dbRequestLayer import request_by_lang_by_date
from const.constants import SUPPORTED_LANGUAGES
from const.constants_langs import DAILY_TWEET_SENTENCE

'''
    daily_tweet
'''
def daily_tweet():

    yesterday = date.today() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y/%m/%d')    

    for lang in SUPPORTED_LANGUAGES:
        
        lines = request_by_lang_by_date(lang, yesterday.year, yesterday.month, yesterday.day)

        top3 = lines.items[:3]
        # Identification du top 3
        medals = ["🥇",  "🥈", "🥉"]
        top3_display = []
        for index, line in enumerate(top3):
            article = line.title.replace("_", " ")
            translation = line.en_translation
            views = line.views
            #if not lang in LANG_LIMIT_TWITTER:
            top3_display.append( [medals[index], article, translation, "{:,}".format(line.views)] )
            #else:
            #top3_display.append( [medals[index], article, views] )
        # On écrit le texte du tweet pour cette langue
        text = DAILY_TWEET_SENTENCE[lang] +  ' '+ f'({yesterday_str})\r\n'
        url = f'https://statswiki.info/{lang}/{yesterday.year}/{yesterday.month}/{yesterday.day}'
        for top in top3_display:
            text += ' '.join([element for element in top]) + '\r\n'    
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