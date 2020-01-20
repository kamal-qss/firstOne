# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TamOct(models.Model):
    appid = models.CharField(max_length=150)
    did = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    sid = models.CharField(max_length=200, blank=True, null=True)
    rtime = models.CharField(max_length=200)
    utime = models.CharField(max_length=200)
    segment = models.TextField()  # This field type is a guess.
    context = models.TextField()  # This field type is a guess.
    eventtime = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'TAM_OCT'


class Croninfo(models.Model):
    maxtimestamp = models.TextField(blank=True, null=True)
    number_of_records = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'croninfo'


class Event(models.Model):
    ideventdata = models.AutoField(primary_key=True)
    device_id = models.TextField(blank=True, null=True)
    timestamp = models.TextField(blank=True, null=True)
    event_key = models.TextField(blank=True, null=True)
    sessionid = models.TextField(blank=True, null=True)
    click_datetime = models.TextField(blank=True, null=True)
    segment_album = models.TextField(blank=True, null=True)
    segment_source = models.TextField(blank=True, null=True)
    segment_pstate = models.TextField(blank=True, null=True)
    segment_app = models.TextField(blank=True, null=True)
    segment_song = models.TextField(blank=True, null=True)
    device_model = models.CharField(max_length=45, blank=True, null=True)
    device_platform = models.CharField(max_length=45, blank=True, null=True)
    device_app_version = models.CharField(max_length=45, blank=True, null=True)
    device_carrier = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.CharField(max_length=45, blank=True, null=True)
    appid = models.CharField(max_length=45, blank=True, null=True)
    slackdata = models.CharField(max_length=45, blank=True, null=True)
    request = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event'


class Events5Ad83Ce1F71De7016Db4C0C1(models.Model):
    appid = models.CharField(max_length=150, blank=True, null=True)
    did = models.CharField(max_length=200, blank=True, null=True)
    key = models.CharField(max_length=200, blank=True, null=True)
    sid = models.CharField(max_length=200, blank=True, null=True)
    rtime = models.IntegerField(blank=True, null=True)
    utime = models.IntegerField(blank=True, null=True)
    segment = models.TextField(blank=True, null=True)  # This field type is a guess.
    context = models.TextField(blank=True, null=True)  # This field type is a guess.
    eventtime = models.IntegerField(blank=True, null=True)
    dt = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events_5ad83ce1f71de7016db4c0c1'


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
    created_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventsdata'


class Fmcompetapps(models.Model):
    appid = models.CharField(db_column='appId', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fmcompetapps'


class Fmpackages(models.Model):
    appid = models.CharField(max_length=150)
    pkg = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    created_at = models.DateField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fmpackages'


class Fmpackagesdemo(models.Model):
    appid = models.CharField(max_length=150, blank=True, null=True)
    # id = models.IntegerField(blank=True, null=True)
    pkg = models.CharField(max_length=200, blank=True, null=True)
    sid = models.CharField(max_length=200, blank=True, null=True)
    f = models.TextField(blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fmpackagesdemo'


class Fmtrackinglist(models.Model):
    appid = models.CharField(max_length=150, blank=True, null=True)
    pkg = models.CharField(max_length=200, blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fmtrackinglist'


class Insertdatacopy(models.Model):
    # id = models.AutoField()
    timestamp = models.TextField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insertdatacopy'


class Installdata(models.Model):
    idinstalldata = models.AutoField(primary_key=True)
    appid = models.TextField(blank=True, null=True)
    timestamp = models.TextField(blank=True, null=True)
    deviceid = models.TextField(blank=True, null=True)
    sdkversion = models.TextField(blank=True, null=True)
    click_datetime = models.TextField(blank=True, null=True)
    metrics = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_date = models.DateTimeField(blank=True, null=True)
    ipaddress = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    device_token = models.TextField(blank=True, null=True)
    age = models.TextField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    registrationdone = models.BooleanField(blank=True)

    class Meta:
        managed = False
        db_table = 'installdata'


class Installdatadummy(models.Model):
    idinstalldata = models.IntegerField()
    appid = models.TextField(blank=True, null=True)
    timestamp = models.TextField(blank=True, null=True)
    deviceid = models.TextField(blank=True, null=True)
    sdkversion = models.TextField(blank=True, null=True)
    click_datetime = models.TextField(blank=True, null=True)
    metrics = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_date = models.DateField(blank=True, null=True)
    ipaddress = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'installdatadummy'


class Mastertabledemo(models.Model):
    station = models.TextField(blank=True, null=True)
    frequency = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mastertabledemo'
