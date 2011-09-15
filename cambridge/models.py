from django.db import models

class CambridgeDocument(db.Model):
    created_date = db.DateTimeProperty(required=True, auto_now_add=True)
    last_access = db.DateTimeProperty(required=True, auto_now_add=True)
    ip = db.StringProperty(required=True)
    original = db.TextProperty(required=True)
    translated = db.TextProperty(required=True)