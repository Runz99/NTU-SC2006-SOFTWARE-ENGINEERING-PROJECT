# Generated by Django 4.1.7 on 2023-03-28 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_review_restaurant_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='restaurant_rating',
            field=models.CharField(max_length=1),
        ),
    ]
