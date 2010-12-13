from google.appengine.ext import db
from default.models import User


class Account(db.Model):
    name = db.StringProperty(required=True)
    owner = db.UserProperty()
    number = db.StringProperty() # Account number. Last four digits will be displayed

    def __str__(self):
        return '%s (%s)' % (self.name, self.number[-4:])
    
class Transaction(db.Model):
    timestamp = db.DateTimeProperty(required=True, auto_now=True)
    owner = db.UserProperty()
    account = db.ReferenceProperty(reference_class=Account)
    transaction_id = db.StringProperty()
    amount = db.FloatProperty(required=True)
    currency = db.CategoryProperty(required=True)
    merchant = db.StringProperty(required=True)
    address = db.PostalAddressProperty()
    phone = db.PhoneNumberProperty()
    category = db.CategoryProperty()
    notes = db.TextProperty()
