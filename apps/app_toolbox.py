from datetime import date, timedelta
from datetime import date
from datetime import timedelta
from const.SUPPORTED_REDIRECTS_BY_LANG import SUPPORTED_REDIRECTS_BY_LANG
from db.dbRequestLayer import request_by_lang_by_qid_by_date, special_request_redirect, request_qid_from_wikidata_table
from objects import Redirect

'''
    check_date_true_access
'''
def check_date_true_access(year, month=0, day=0):

    today = date.today()
    yesterday = today - timedelta(days = 1)
    start_2015 = date(2015,7, 1)
    
    if day:
        dt = date(year=year, month=month, day=day)
        if dt > yesterday or dt < start_2015:
            return False
    elif month:
        dt = date(year=year, month=month, day=1)
        if dt > yesterday or dt < start_2015:
            return False
    else:
        if year > 2024 or year < 2015:
            return False
    return True


'''
    display
'''
def display(lang, lines, year=0, month=0, day=0):

    lines_to_add = []
    lines_to_remove = []

    for line in lines.items:

        qid = line.qid
        title = line.title
        #en_translation = line.en_translation
        views = line.views

        if not title:
            # Car rare mais possible d'un article qui a été supprimé depuis
            # Par exemple Q96379955 en 'ar' p.e
            lines_to_remove.append(line)
        
        elif not views:
            # Est-ce possible ?
            lines_to_remove.append(line)

        else:

            if not qid:
                print(f"if not qid: {line} ")
                lines_to_remove.append(line)

            else:

                if line.is_straight_qid() or line.is_shadow_qid():
 
                    qid_main_redirect = SUPPORTED_REDIRECTS_BY_LANG[lang].get(line.title_with_spaces, {})

                    if qid_main_redirect:
                            
                            if line.is_straight_qid():
                                lines_to_remove.append(line)

                            # On demande les données de l'article principal
                            main_redirect_lines = request_by_lang_by_qid_by_date(lang, qid_main_redirect, year, month, day)
                            
                            if main_redirect_lines.items:
                                main_redirect_line = main_redirect_lines.items[0]
                                if not lines.is_qid_included(qid_main_redirect):
                                    lines_to_add.append(main_redirect_line)
                            
                            else:
                                # On a pas de données sur l'article dans la table-ci
                                # On demande à _wikidata             
                                lines_seconde_chance = request_qid_from_wikidata_table(lang, qid_main_redirect)

                                if main_redirect_lines.items:
                                    main_redirect_line = main_redirect_lines.items[0]
                                    if not lines.is_qid_included(qid_main_redirect):
                                        lines_to_add.append(main_redirect_line)
                # End if IS_STRAIGHT_QID or IS_SHADOW_QID:
                else:
                    # On a un article qui existe avec un qid qui existe
                    print(f"Line 222, app.py {qid} {title}")

    for line in lines_to_remove:
        print(f'line removed {line}')
        lines.remove(line)

    for line in lines_to_add:
        print(f'line added {line}')
        lines.add(line)         
    
    # redirects     
    for line in lines.items:

        qid = line.qid

        for redir, qid_ in SUPPORTED_REDIRECTS_BY_LANG[lang].items():
                if qid == qid_:
                    redir_title = redir.replace(" ", "_")
                    lines_redir_views = special_request_redirect(
                                                lang,
                                                redir_title,
                                                year,
                                                month,
                                                day)
                    
                    if lines_redir_views.items:
                        redir_views = lines_redir_views.items[0].views
                        line.redirects.add(Redirect(redir_title, redir_views))
                        line.views += redir_views
                    else:
                        line.redirects.add(Redirect(redir_title, 0))

    # sort
    lines.items = lines.items[:50]
    lines.items.sort(key=lambda line: line.views, reverse=True)

    # format us 
    for line in lines.items: 
        line.views = "{:,}".format(line.views)    
        for redir in line.redirects.items:
            redir.views = "{:,}".format(redir.views)

    return lines


'''
    check_results
'''
def check_results(results):

    try:
        if results is None:
            return False
        if results == []:
            return False
        else:
            return True
    except Exception as e:
        print(f'{e} check_results line 224')    
        return False
    