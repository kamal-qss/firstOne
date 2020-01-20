# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Apps(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    installs = models.BigIntegerField(blank=True, null=True)
    uninstalls = models.BigIntegerField(blank=True, null=True)
    appid = models.CharField(max_length=250, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    createdat = models.DateTimeField(blank=True, null=True)
    updatedat = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'apps'


class Dataset(models.Model):
    appid = models.CharField(max_length=150, blank=True, null=True)
    fullname = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset'


class Eventsdata(models.Model):
    appid = models.CharField(max_length=150, blank=True, null=True)
    events = models.TextField(blank=True, null=True)  # This field type is a guess.
    device_id = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.CharField(max_length=200, blank=True, null=True)
    mtimestamp = models.CharField(max_length=200, blank=True, null=True)
    uptimestamp = models.CharField(max_length=200, blank=True, null=True)
    ipaddress = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    eventname = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.CharField(max_length=200, blank=True, null=True)
    updatedate = models.DateField(blank=True, null=True)
    created_time = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventsdata'


class Fmpackagesdemo(models.Model):
    appid = models.CharField(max_length=150, blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)
    pkg = models.CharField(max_length=200, blank=True, null=True)
    sid = models.CharField(max_length=200, blank=True, null=True)
    f = models.CharField(max_length=-1, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fmpackagesdemo'


class Fmpackageslist(models.Model):
    appid = models.CharField(max_length=150, blank=True, null=True)
    pkg = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=-1, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fmpackageslist'


class Installdata(models.Model):
    idinstalldata = models.AutoField(primary_key=True)
    appid = models.CharField(max_length=-1, blank=True, null=True)
    timestamp = models.CharField(max_length=-1, blank=True, null=True)
    deviceid = models.CharField(max_length=-1, blank=True, null=True)
    sdkversion = models.CharField(max_length=-1, blank=True, null=True)
    click_datetime = models.CharField(max_length=-1, blank=True, null=True)
    metrics = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_date = models.DateField(blank=True, null=True)
    ipaddress = models.CharField(max_length=-1, blank=True, null=True)
    city = models.CharField(max_length=-1, blank=True, null=True)
    country = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'installdata'


class Mastertabledemo(models.Model):
    station = models.CharField(max_length=200, blank=True, null=True)
    frequency = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mastertabledemo'


class Users(models.Model):
    appid = models.CharField(max_length=150, blank=True, null=True)
    fullname = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
