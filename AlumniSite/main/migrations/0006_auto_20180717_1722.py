# Generated by Django 2.0.1 on 2018-07-17 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180717_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='createur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
