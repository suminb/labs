from django.db import models
from default.models import User

class Report(db.Model):
    name = db.StringProperty(required=True)
    description = db.TextProperty()
    birthdate = db.DateProperty()
    deathdate = db.DateProperty()
    sex = db.StringProperty(required=True, choices=set(['female', 'male', 'na']))
    images = db.StringListProperty() # urls of images
    links = db.StringListProperty() # urls
    group = db.ReferenceProperty()
    
class System(db.Model):
    name = db.StringProperty(required=True) # hostname
    description = db.TextProperty()
    owner = db.UserProperty()
    