import requests
from constants import SUPPORTED_LANGUAGES
from constants_wikidata import WIKIDATA_PROPERTIES
import json

'''
    get_qid
'''
def get_qid(lang, tuple_article_views):
    
    article = tuple_article_views[0]
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
    get_main_properties
'''
def get_main_properties(lang, claims, qid):

    dprops = WIKIDATA_PROPERTIES['direct']
    ndprops = WIKIDATA_PROPERTIES['non_direct']
    
    direct_props = list(set(dprops.keys()).intersection(claims.keys()))
    non_direct_props = list(set(ndprops.keys()).intersection(claims.keys()))

    results = {}

    for prop in direct_props:

        claim = claims[prop]
        
        # 'snaktype': 'datavalue': 'value':        
        claim_mainsnak = list(claim[0].values())[0]
        claim_value = ""
        try:
            claim_value = str(claim_mainsnak['datavalue']['value'])
        except Exception as e:
            print(f"direct_prop ['datavalue']['value']: {lang}-{qid}")
        results[prop] = claim_value

    for prop in non_direct_props:

        claim = claims[prop]
        # [{'mainsnak': {'snaktype': 'novalue', 'property': 'P17', 'hash': '9bd0d5bb5273ae454d4fbf369b5913462e400339', 'datatype': 'wikibase-item'}, 'type': 'statement', 'id': 'Q46$aede7db1-4cf4-163a-a357-a991a592a336', 'rank': 'normal'}]
        condition = claim[0]['mainsnak']['snaktype']
        if condition == 'value':
            claim_value = claim[0]['mainsnak']['datavalue']['value']['id']
            results[prop] = claim_value
        else:
            results[prop] = ''


    return json.dumps(results)


'''
    get_wikidata_stuff
'''
def get_wikidata_stuff(lang, qid):

    base_url = 'https://www.wikidata.org/w/api.php'

    # label_en
    response = requests.get(url=base_url, params={
        'action': 'wbgetentities',
        'ids': qid,  
        'languages': 'en',  
        'props': 'labels',
        'format': 'json'
    })
    data = response.json()
    first = data['entities'][qid]['labels'].get('en', {})
    label_en = ''
    if first:
        label_en = first['value']
    # label_en ok


    # props, images
    response = requests.get(url=base_url, params={
        'action': 'wbgetentities',
        'ids': qid,
        'languages': lang,
        'props': 'claims',
        'format': 'json'
    })
    data = response.json()
    claims = data['entities'][qid]['claims']
    main_properties = get_main_properties(lang, claims, qid)
    # props, images ok

    # Les interwikis
    response = requests.get(url=base_url, params={
        'action': 'wbgetentities',
        'ids': qid,
        'props': 'sitelinks',
        'format': 'json'
    })
    data = response.json()
    sitelinks = data['entities'][qid]['sitelinks']
    
    return {
        'label_en': label_en,
        'main_properties': main_properties,
        'sitelinks': sitelinks
    }

    
