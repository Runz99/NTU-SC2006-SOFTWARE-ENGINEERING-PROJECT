# Generated by Django 3.2.18 on 2023-03-03 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_restaurantname_restaurantdb_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurantdb',
            old_name='openingHours',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='restaurantdb',
            old_name='restaurantAddress',
            new_name='cuisine',
        ),
        migrations.RenameField(
            model_name='restaurantdb',
            old_name='restaurantCuisine',
            new_name='opening_hours',
        ),
        migrations.RenameField(
            model_name='restaurantdb',
            old_name='restaurantID',
            new_name='rating',
        ),
        migrations.RemoveField(
            model_name='restaurantdb',
            name='restaurantRating',
        ),
    ]