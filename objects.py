import re

'''
    Redirect
'''
class Redirect:
    def __init__(self, 
                 title, 
                 views=0):
        self.title = title
        self.views = views
    def __repr__(self):
        return f"Redirect:{self.title}|{self.views}\n"

'''
    Redirects
'''
class Redirects:
    def __init__(self):
        self.items = []

    def add(self, item):
        if isinstance(item, Redirect):
            self.items.append(item)
        else:
            raise ValueError("class Redirects: Not an instance of Redirect")

    def remove(self, item):
        self.items.remove(item)

    def __repr__(self):
        return f"Redirects:{self.items}\n"

'''
    Line
'''
class Line:
    def __init__(self, 
                 qid='', 
                 title='', 
                 en_translation='', 
                 views=0, 
                 props='',
                 wikidata_image='',
                 wikidata_image_url = ''):
        self.qid = qid
        self.title = title
        self.en_translation = en_translation
        self.views = views,
        self.props = props,
        self.wikidata_image = wikidata_image
        self.wikidata_image_url = wikidata_image_url
        self.redirects = Redirects()

    def __repr__(self):
        return f"Line:{self.qid}|{self.title}|{self.en_translation}|{self.views}|{self.wikidata_image}|{self.wikidata_image_url}\n{self.redirects}"
    
    def is_straight_qid(self):
        motif_straight = r'^Q\d+$'
        if re.match(motif_straight, self.qid):
            return True
        return False
    
    def is_shadow_qid(self):
        if self.qid.startswith(f"Q_"):
            return True
        return False
    

'''
    Lines
'''
class Lines:
    def __init__(self, lang, year=0, month=0, day=0):
        self.lang = lang,
        self.year = year,
        self.month = month,
        self.day = day,         
        self.items = []

    def add(self, item):
        if isinstance(item, Line):
            self.items.append(item)
        else:
            raise ValueError("class Lines: Not an instance of Line")

    def remove(self, item):
        self.items.remove(item)

    def __repr__(self):
        return f"Lines:{self.lang}|{self.year}|{self.month}|{self.day}\n{self.items}"
    
    def is_qid_included(self, qid):
        for line in self.items:
            if line.qid == qid:
                return True
