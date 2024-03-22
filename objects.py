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

    def to_dict(self):
        return {
            "title" : self.title,
            "views" : self.views
        }


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

    def to_dict(self):
        return [redirect.to_dict() for redirect in self.items[:20]]


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
                 wikidata_image_url = '',
                 views_collection = []):
        self.qid = qid
        self.title = title
        self.en_translation = en_translation
        self.views = views,
        self.props = props,
        self.wikidata_image = wikidata_image
        self.wikidata_image_url = wikidata_image_url
        self.redirects = Redirects()
        self.views_collection = views_collection

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
    
    @property
    def title_with_spaces(self):
        return self.title.replace("_", " ")
    
    @property
    def title_with_undescores(self):
        return self.title.replace(" ", "_")

    def to_dict(self):
        return {
            "qid": self.qid,
            "title": self.title,
            "views": self.views,
            "en_translation" : self.en_translation,
            "props" : self.props,
            "wikidata_image" : self.wikidata_image,
            "wikidata_image_url" : self.wikidata_image_url,
            "redirects" : self.redirects.to_dict(),
            "views_collection" : [views_collection.to_dict() for views_collection in self.views_collection]
        }
    

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

    def to_dict(self):
        return {
            "lang" : self.lang,
            "year" : self.year,
            "month" : self.month,
            "day" : self.day,
            "items" : [item.to_dict() for item in self.items]
        }
