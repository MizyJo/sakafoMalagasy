# Generated by Django 5.0.2 on 2024-03-18 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0010_recette_accomplie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recette_accomplie',
            name='recette',
        ),
        migrations.AddField(
            model_name='recette_accomplie',
            name='recette',
            field=models.ManyToManyField(to='membre.recette'),
        ),
    ]
