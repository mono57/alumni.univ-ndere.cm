# Generated by Django 2.0.1 on 2018-07-12 09:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20180712_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 12, 9, 12, 57, 663595, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 12, 9, 12, 57, 663489)),
        ),
    ]