# Generated by Django 5.0.2 on 2024-03-05 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membre', '0004_alter_photo_fichier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='fichier',
            field=models.ImageField(upload_to='image_recette'),
        ),
    ]