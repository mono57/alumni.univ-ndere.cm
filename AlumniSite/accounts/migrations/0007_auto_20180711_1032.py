# Generated by Django 2.0.1 on 2018-07-11 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20180711_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etudiant',
            name='mot_de_passe1',
        ),
        migrations.RemoveField(
            model_name='etudiant',
            name='mot_de_passe2',
        ),
        migrations.AddField(
            model_name='etudiant',
            name='mot_de_passe',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
