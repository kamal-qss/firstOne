# Generated by Django 2.1.7 on 2019-04-22 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GetData', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Croninfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maxtimestamp', models.TextField(blank=True, null=True)),
                ('number_of_records', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'croninfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('ideventdata', models.AutoField(primary_key=True, serialize=False)),
                ('device_id', models.TextField(blank=True, null=True)),
                ('timestamp', models.TextField(blank=True, null=True)),
                ('event_key', models.TextField(blank=True, null=True)),
                ('sessionid', models.TextField(blank=True, null=True)),
                ('click_datetime', models.TextField(blank=True, null=True)),
                ('segment_album', models.TextField(blank=True, null=True)),
                ('segment_source', models.TextField(blank=True, null=True)),
                ('segment_pstate', models.TextField(blank=True, null=True)),
                ('segment_app', models.TextField(blank=True, null=True)),
                ('segment_song', models.TextField(blank=True, null=True)),
                ('device_model', models.CharField(blank=True, max_length=45, null=True)),
                ('device_platform', models.CharField(blank=True, max_length=45, null=True)),
                ('device_app_version', models.CharField(blank=True, max_length=45, null=True)),
                ('device_carrier', models.CharField(blank=True, max_length=45, null=True)),
                ('created_date', models.CharField(blank=True, max_length=45, null=True)),
                ('appid', models.CharField(blank=True, max_length=45, null=True)),
                ('slackdata', models.CharField(blank=True, max_length=45, null=True)),
                ('request', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'event',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Events5Ad83Ce1F71De7016Db4C0C1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appid', models.CharField(blank=True, max_length=150, null=True)),
                ('did', models.CharField(blank=True, max_length=200, null=True)),
                ('key', models.CharField(blank=True, max_length=200, null=True)),
                ('sid', models.CharField(blank=True, max_length=200, null=True)),
                ('rtime', models.IntegerField(blank=True, null=True)),
                ('utime', models.IntegerField(blank=True, null=True)),
                ('segment', models.TextField(blank=True, null=True)),
                ('context', models.TextField(blank=True, null=True)),
                ('eventtime', models.IntegerField(blank=True, null=True)),
                ('dt', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'events_5ad83ce1f71de7016db4c0c1',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Fmcompetapps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appid', models.CharField(blank=True, db_column='appId', max_length=45, null=True)),
            ],
            options={
                'db_table': 'fmcompetapps',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Fmpackages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appid', models.CharField(max_length=150)),
                ('pkg', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=100)),
                ('created_at', models.DateField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'fmpackages',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Fmtrackinglist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appid', models.CharField(blank=True, max_length=150, null=True)),
                ('pkg', models.CharField(blank=True, max_length=200, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('create_date', models.DateField(blank=True, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'fmtrackinglist',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Insertdatacopy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.TextField(blank=True, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'insertdatacopy',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Installdatadummy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idinstalldata', models.IntegerField()),
                ('appid', models.TextField(blank=True, null=True)),
                ('timestamp', models.TextField(blank=True, null=True)),
                ('deviceid', models.TextField(blank=True, null=True)),
                ('sdkversion', models.TextField(blank=True, null=True)),
                ('click_datetime', models.TextField(blank=True, null=True)),
                ('metrics', models.TextField(blank=True, null=True)),
                ('created_date', models.DateField(blank=True, null=True)),
                ('ipaddress', models.TextField(blank=True, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'installdatadummy',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TamOct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appid', models.CharField(max_length=150)),
                ('did', models.CharField(max_length=200)),
                ('key', models.CharField(max_length=200)),
                ('sid', models.CharField(blank=True, max_length=200, null=True)),
                ('rtime', models.CharField(max_length=200)),
                ('utime', models.CharField(max_length=200)),
                ('segment', models.TextField()),
                ('context', models.TextField()),
                ('eventtime', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'TAM_OCT',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(blank=True, max_length=200, null=True)),
                ('app_id', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('otp', models.TextField(blank=True, null=True)),
                ('contact_no', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'userprofile',
                'managed': False,
            },
        ),
    ]
