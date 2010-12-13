from django.db import models

class Rainbowtable(models.Model):
    id = models.IntegerField(primary_key=True)
    plain = models.CharField(unique=True, max_length=255)
    md5 = models.CharField(max_length=72, blank=True)
    sha1 = models.CharField(max_length=84, blank=True)
    class Meta:
        db_table = u'rainbowtable'
