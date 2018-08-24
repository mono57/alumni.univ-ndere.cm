# Generated by Django 2.0.1 on 2018-08-11 23:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0024_remove_inscription_alumni'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscription',
            name='alumni',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
