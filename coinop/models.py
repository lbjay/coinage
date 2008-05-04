from django.db import models
from datetime import datetime
from collector.models import Site

# Create your models here.

class RegistryCache(models.Model):
    cacheid = models.IntegerField(primary_key=True)
    ip = models.IPAddressField()
    entrytime = models.DateTimeField(default=datetime.now)
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

# Create your models here.
