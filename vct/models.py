from google.appengine.ext import db
from appengine_django.models import BaseModel

from default.models import User

class Vehicle(db.Model):
    year = db.IntegerProperty(required=True)
    make = db.StringProperty(required=True)
    model = db.StringProperty(required=True)
    trim = db.StringProperty()
    type = db.StringProperty()
    price = db.IntegerProperty()

    tags = db.StringListProperty()
    pictures = db.StringListProperty()

    def __str__(self):
        return '%d %s %s' % (self.year, self.make, self.model)
    
class Choice(BaseModel):
    name = db.StringProperty()
    image = db.LinkProperty()
    image_source = db.LinkProperty()
    tags = db.StringListProperty()
    counts = db.ListProperty(item_type=int)
    
class Question(db.Model):
    question = db.StringProperty(required=True)
    description = db.TextProperty()
    choices = db.ListProperty(item_type=db.Key) # may have more than two choices, but we'll limit to be two for now

    def tags(self):
        return []
    
#class Tag(db.Model):
#    name = db.StringProperty(required=True)

class Questionnaire(db.Model):
    timestamp = db.DateTimeProperty(required=True, auto_now=True)
    raw_data = db.TextProperty()


class Result(db.Model):
    vehicle = db.StringProperty(required=True)
    queries = db.TextProperty()
    
    
# tags
#
# luxury, basic, essential
# sporty, nimble, agile
# comfortable
# affordable
# masculine, feminine
# angular, round
# eco-friendly, pollutant
# well-equipped

# special vehicle candidates
#
# bumble bee
# optimus prime
# roman horse race thing

