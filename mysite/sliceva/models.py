from django.db import models

# Create your models here.

class Device(models.Model):
    host = models.CharField(max_length=50, db_index=True, null=False)
    loginmethod = models.CharField(max_length=20, null=False)

    def __unicode__(self):
        return self.host

class User(models.Model):
    username = models.CharField(max_length=20, db_index=True, null=False)
    password = models.CharField(max_length=30, null=False)
    admin = models.BooleanField(null=False, default=False)

    def __unicode__(self):
        return self.username

class Log(models.Model):
    host = models.CharField(max_length=50, db_index=True, null=False)
    entry = models.TextField(max_length=500, null=False)

    def __unicode__(self):
        return self.entry

