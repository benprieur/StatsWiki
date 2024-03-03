from datetime import datetime, timedelta
from DatabaseRequest import request_data_date_lang, request_data_month_lang
from datetime import date
import tweepy
from GlobalData import SUPPORTED_LANGUAGES, DAILY_TWEET_SENTENCE, MONTHS_BY_LANG, MONTHLY_TWEET_SENTENCE
import time

'''
    daily_tweet
'''
def daily_tweet():
    yesterday = date.today() - timedelta(days=1)
    #print(yesterday) #2024-02-27

    for lang in SUPPORTED_LANGUAGES:
        
        # Tweet
        results = []
        try:
            smonth = f'{yesterday.month:02d}'
            sday = f'{yesterday.day:02d}'
            syear = str(yesterday.year)
            results = request_data_date_lang(lang, syear, smonth, sday)
        except Exception as e:
            print(f"{e}")
            results = []
            return

        if results[0][1] == 0:
            results = []
            return
        
        articles = []
        text = ''
        for item in results[:3]:
            article = item[0]
            views = item[1]            
            article_with_spaces = article.replace("_", " ")
            articles.append([article_with_spaces, views])     


            yesterday_str = yesterday.strftime('%Y/%m/%d')
            text = DAILY_TWEET_SENTENCE[lang] +  ' '+ f'({yesterday_str})\n'

            url = f'http://statswiki.info/{lang}/{yesterday.year}/{yesterday.month}/{yesterday.day}'
            for index, article in enumerate(articles, start=1):
                match (index):
                    case 1: text += "🥇 "
                    case 2: text += "🥈 "
                    case 3: text += "🥉 "
                text += f"{article[0]} ({article[1]})"  + "\n"
            text += url + "\n"
        print(text)
        tweet_upload_v2(text)
        

'''
    monthly_tweet
'''
def monthly_tweet():
    last_month = date.today() - timedelta(days=2)

    for lang in SUPPORTED_LANGUAGES:
        
        # Tweet
        results = []
        try:
            smonth = f'{last_month.month:02d}'
            syear = str(last_month.year)
            results = request_data_month_lang(lang, syear, smonth)
        except Exception as e:
            print(f"{e}")
            results = []
            return

        if results[0][1] == 0:
            results = []
            return
        
        articles = []
        text = ''
        for item in results[:3]:
            article = item[0]
            views = item[1]            
            article_with_spaces = article.replace("_", " ")
            articles.append([article_with_spaces, views])     


            last_month_str = MONTHS_BY_LANG[lang][last_month.month-1] + ' ' + syear
            text = MONTHLY_TWEET_SENTENCE[lang] +  ' ' + f'{last_month_str}\n'

            article_url = f'http://statswiki.info/{lang}/{last_month.year}/{last_month.month}'
            for index, article in enumerate(articles, start=1):
                match (index):
                    case 1: text += "🥇 "
                    case 2: text += "🥈 "
                    case 3: text += "🥉 "
                text += f"{article[0]} ({article[1]})"  + "\n"
            text += article_url + "\n"
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