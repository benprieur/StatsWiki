import requests
from constants import SUPPORTED_LANGUAGES
from constants_wikidata import SUPPORTED_WIKIDATA_PROPERTIES
import json

'''
    get_qid
'''
def get_qid(lang, article):
    url = f'https://{lang}.wikipedia.org/w/api.php?action=query&titles={article}&prop=pageprops&format=json'

    try:
        headers = {'User-Agent': 'MyApp/1.0 (myemail@example.com)'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            try:
                pages = data['query']['pages']
                pageid = ''

                for page in pages.values():
                    pageid = page['pageid']
                    break
            except:
                print(f'get_qid exception - pageid: {lang} {article}')
                return '', ''
            try:
                wikidata = pages[f'{pageid}']['pageprops']['wikibase_item']
            except:
                print(f'get_qid exception - wikibase_item: {lang} {article}')
                return '', ''
            return pageid, wikidata
    except requests.RequestException as e:
        print(f"{e}") 
        return '', '' 
    

'''
    get_sitelinks
'''
def get_sitelinks(input_dict):
    modified_dict = {}
    for lang, data in input_dict.items():
        lang_short = lang.replace('wiki', '')
        modified_title = data['title'].replace(' ', '_')  
        modified_dict[lang_short] = modified_title
    
    modified_dict = {lang: title for lang, title in modified_dict.items() if lang in SUPPORTED_LANGUAGES}

    return modified_dict

'''
    get_main_properties
'''
def get_main_properties(lang, claims):

    base_url = 'https://www.wikidata.org/w/api.php'
    props = list(set(SUPPORTED_WIKIDATA_PROPERTIES.keys()).intersection(claims.keys()))

    results = {}
    for prop in props:
        claim = claims[prop]
        claim_mainsnak = list(claim[0].values())[0]
        claim_value = str(claim_mainsnak['datavalue']['value'])
        results[prop] = claim_value

    return json.dumps(results)


'''
    get_wikidata_stuff
'''
def get_wikidata_stuff(lang, qid):
    
    try:
        base_url = 'https://www.wikidata.org/w/api.php'
        
        # Le label (en) dans Wikidata
        response_labels = requests.get(url=base_url, params={
            'action': 'wbgetentities',
            'ids': qid,
            'languages': 'en',
            'props': 'labels',
            'format': 'json'
        }).json()
        label_en = response_labels['entities'][qid]['labels'].get('en', {}).get('value', '')
        
        # Les props intéressantes
        response_claims = requests.get(url=base_url, params={
            'action': 'wbgetentities',
            'ids': qid,
            'languages': lang,
            'props': 'claims',
            'format': 'json'
        }).json()
        claims = response_claims['entities'][qid].get('claims', {})
        main_properties = get_main_properties(lang, claims)
        
        # Les interwikis
        response_sitelinks = requests.get(url=base_url, params={
            'action': 'wbgetentities',
            'ids': qid,
            'props': 'sitelinks',
            'format': 'json'
        }).json()
        
        sitelinks = response_sitelinks['entities'][qid].get('sitelinks', {})
        modified_sitelinks = get_sitelinks(sitelinks)

        return {
            'label_en': label_en,
            'main_properties': main_properties,
            'sitelinks': modified_sitelinks
        }
    except:
        return {}