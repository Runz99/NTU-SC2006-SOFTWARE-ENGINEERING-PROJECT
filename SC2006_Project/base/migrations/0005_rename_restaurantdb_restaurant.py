# Generated by Django 4.1.7 on 2023-03-20 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_rating_restaurantdb_restaurant_rating'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='restaurantDB',
            new_name='restaurant',
        ),
    ]