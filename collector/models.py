from django.db import models
from datetime import datetime

# Create your models here.

class Site(models.Model):
    siteid = models.IntegerField()
    sitename = models.CharField(max_length=32)
    def url(self):
        return "/collector/site/%s" % self.sitename
    def __unicode__(self):
        return self.sitename
    class Admin:
        pass


class Ctxo(models.Model):
    ctxoid = models.IntegerField()
    couchid = models.IntegerField()
    timestamp = models.DateTimeField(default=datetime.now)
    siteid = models.ForeignKey(Site)
    ctxo = models.TextField()
    class Admin:
        pass
