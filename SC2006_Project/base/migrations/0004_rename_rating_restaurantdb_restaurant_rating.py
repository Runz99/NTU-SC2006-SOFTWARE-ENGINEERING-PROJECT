# Generated by Django 3.2.18 on 2023-03-03 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20230303_2039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurantdb',
            old_name='rating',
            new_name='restaurant_rating',
        ),
    ]
