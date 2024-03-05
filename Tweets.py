from datetime import datetime, timedelta
from dbRequestLayer import request_by_lang_by_day, request_by_lang_by_month
from datetime import date
import tweepy
from constants import SUPPORTED_LANGUAGES, DAILY_TWEET_SENTENCE, MONTHS_BY_LANG, MONTHLY_TWEET_SENTENCE
import time

'''
    daily_tweet
'''
def daily_tweet():
    yesterday = date.today() - timedelta(days=1)
    #print(yesterday) #2024-02-27

    for lang in SUPPORTED_LANGUAGES:
        
        results = request_by_lang_by_day(lang, 
                                        yesterday.year, 
                                        yesterday.month, 
                                        yesterday.day,
                                        translation=True)
        
        articles = []
        for article in results:
                article_with_ = article[0]
                article_with_space = article[0].replace("_", " ")
                views = article[1]
                translation = article[2] if article[2] else ""
                articles.append([article_with_, 
                                article_with_space, 
                                views, 
                                translation])       


        yesterday_str = yesterday.strftime('%Y/%m/%d')
        
        text = DAILY_TWEET_SENTENCE[lang] +  ' '+ f'({yesterday_str})\n'
        url = f'http://statswiki.info/{lang}/{yesterday.year}/{yesterday.month}/{yesterday.day}'
        for index in range(0, 3):
            match (index):
                case 0: text += "🥇 "
                case 1: text += "🥈 "
                case 2: text += "🥉 "
            text += f'{articles[index][1]}' 
            if lang in ['ar', 'ja', 'he', 'hy', 'ko', 'nl', 'ru', 'uk', 'zh']:
                text += f' {articles[index][3]}\n'
            else:
                text += f'\n'   
        text += f'{url}\n'
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