from google.appengine.ext import db

class MarkdownDocument(db.Model):
    timestamp = db.DateTimeProperty(required=True, auto_now_add=True)
    ip = db.StringProperty(required=True)
    content = db.TextProperty(required=True)