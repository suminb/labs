from google.appengine.ext import db
from datetime import date, timedelta
from django.utils import simplejson as json

class Person(db.Model):
    name = db.StringProperty(required=True)
    description = db.TextProperty()
    birthdate = db.DateProperty()
    deathdate = db.DateProperty()
    sex = db.StringProperty(required=True, choices=set(['female', 'male', 'na']))
    images = db.StringListProperty() # urls of images
    links = db.StringListProperty() # urls
    group = db.ReferenceProperty()

    #author = db.ReferenceProperty()
    last_updated = db.DateTimeProperty()
    
    def to_dict(self):
        o = dict([('key', str(self.key()))] + [(p, unicode(getattr(self, p))) if getattr(self, p) != None else (p, None) for p in self.properties()])
        o['images'] = self.images
        o['links'] = self.links
        
        return o
    
    @staticmethod
    def fetch_by_birthdate(year, month, day, within):
        rows = []

        q = Person.all().filter(
                'birthdate >', date(year, month, day) - timedelta(within * 365)
            ).filter(
                'birthdate <', date(year, month, day) + timedelta(within * 365)
            )
        for person in q.fetch(100):
            rows.append(person)

        return rows
    
    @staticmethod
    # page: zero-based page number
    # n: number of entries for each page
    #
    # FIXME: This function will not work when the offset (page*n) exceeds 1000.
    def fetch_page(page, n=25):
        q = Person.all()
        
        return q.fetch(n, page*n)
    
class Group(db.Model):
    name = db.StringProperty(required=True)
    images = db.StringListProperty() # urls of images
    links = db.StringListProperty() # urls