from django.db import models
from datetime import datetime

# Create your models here.

class Item(models.Model):
    id = models.IntegerField(primary_key = True)
    def url(self):
        return "/conjure/item/%s" % self.id
    class Admin:
        pass

class Tag(models.Model):
    id = models.IntegerField(primary_key = True)
    def url(self):
        return "/conjure/tag/%s" % self.id
    class Admin:
        pass

class ItemTag(models.Model):
    id = models.IntegerField(primary_key = True)
    itemid = models.ForeignKey(Item)
    tagid = models.ForeignKey(Tag)
    user = models.CharField(max_length=32)
    timestamp = models.DateTimeField(default=datetime.now)
