from DatabaseRequest import request_data_year_lang, request_data_month_lang, get_articles_ranking_by_lang
from GlobalData import SUPPORTED_LANGUAGES, DB_NAME, SUPPORTED_YEARS
from app import check_results
import openai
import json
import sqlite3
import time

'''
  addTradExists
'''
def addTradExists(article, lang):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    check_request = '''SELECT * FROM Translation WHERE article = ? AND lang = ?'''
    cursor.execute(check_request, (article, lang))
    result = cursor.fetchone()
    conn.commit()
    
    conn.close()

    if result:
        return True
    return False 


'''
    addTrad
'''
def addTrad(article, translation, lang):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()


    request = '''INSERT INTO Translation (article, translation, lang) 
                        VALUES (?, ?, ?)'''
    data = (article, translation, lang)

    try:
        cursor.execute(request, data)
        conn.commit()
        print(f"....{article} - {translation} - {lang} => inserted")
    except sqlite3.Error as e:
        print(f"Error during translation insertion: {e}")

    conn.close()



'''
    get_translations
'''
def get_translations(article, lang):
    openai.api_key = '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'
    question = f"Translate in English the title of this Wikipedia article titled {article} in {lang}. Answer only the translation. If you don't know at all, answer A23B45D. If it is already in English, answer ''."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are my assistant in charge to translate in English a term"},
            {"role": "user", "content": question},
        ]
    )
    time.sleep(1)
    answer = response.choices[0].message['content']
    return answer


'''
    evaluate_translationcle
'''
def evaluate_translation(trad):
    if 'A23B45D' in trad:
        return False
    return True


'''
    feedTraductionsTable
'''
def feedTraductionsTable():
    for lang in reversed(SUPPORTED_LANGUAGES):
        if lang != 'en':
            
            for year in [2024, 2023, 2022, 2015, 2016, 2017, 2018, 2019, 2020, 2021]:
                results = get_articles_ranking_by_lang(lang)
                articles = [item[0].replace("_", " ") for item in results if check_results(results)]
                print(f'{lang}-{year}- .')
                for article in articles:         
                    if addTradExists(article, lang) == False:
                        print(f'..')
                        answer = get_translations(article, lang)
                        if (evaluate_translation(answer)):
                            print(f'...')
                            addTrad(article, answer, lang)
 
feedTraductionsTable()

