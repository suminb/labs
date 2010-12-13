from google.appengine.ext import db

class User(db.Model):
    email = db.EmailProperty()
    givenname = db.StringProperty()
    familyname = db.StringProperty()

    def __str__(self):
        return '%s, %s' % (self.familyname, self.givenname)


class Application(db.Model):
    guid = db.StringProperty(required=True)
    access_count = db.IntegerProperty()