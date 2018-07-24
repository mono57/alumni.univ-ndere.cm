# Generated by Django 2.0.1 on 2018-07-24 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20180716_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etudiant',
            name='annee_sortie',
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='annee_entree',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='diplome',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='entreprise',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='faculte',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='fonction',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='matricule',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='residence',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
