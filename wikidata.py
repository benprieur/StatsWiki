import requests
from constants_wikidata import WIKIDATA_PROPERTIES
import json
from constants import REDIRECTS_OUTPUT_FILE

'''
    get_qid
'''
def get_qid(lang, article):

    #print(f'article {article}')
    url = f'https://{lang}.wikipedia.org/w/api.php?action=query&titles={article}&prop=pageprops&format=json'

    headers = {'User-Agent': 'MyApp/1.0 (myemail@example.com)'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:

        pageid = ""
        wikidata = ""

        data = response.json()
        pages = data['query']['pages']
        for page in pages.values():
            #print(page)
            pageid = page.get('pageid', "")
            break
        
        if not pageid:
            return "", ""
        else:
            try:
                wikidata = pages[f'{pageid}']['pageprops']['wikibase_item']
                return pageid, wikidata
            except:
                wikidata = f"Q_{lang}_" + str(article)
                #with open(REDIRECTS_OUTPUT_FILE, 'a') as file:
                #    file.write(f"{lang}-{wikidata}: {article} \n")
                return pageid, wikidata
    

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
    label_en = ''
    try:
        first = data['entities'][qid]['labels'].get('en', {})
        if first:
            label_en = first['value']
    except:
        with open(REDIRECTS_OUTPUT_FILE, 'a') as file:
            file.write(f"{lang}-{qid}\n")
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
    main_properties = None
    try:
        claims = data['entities'][qid]['claims']
        main_properties = get_main_properties(lang, claims, qid)
    except:
        with open(REDIRECTS_OUTPUT_FILE, 'a') as file:
            file.write(f"{lang}-{qid}\n")
    # props, images ok

    # Les interwikis
    response = requests.get(url=base_url, params={
        'action': 'wbgetentities',
        'ids': qid,
        'props': 'sitelinks',
        'format': 'json'
    })
    data = response.json()
    sitelinks = None
    try:
        sitelinks = data['entities'][qid]['sitelinks']
    except:
        with open(REDIRECTS_OUTPUT_FILE, 'a') as file:
            file.write(f"{lang}-{qid}\n")


    
    return {
        'label_en': label_en,
        'main_properties': main_properties,
        'sitelinks': sitelinks
    }

    
