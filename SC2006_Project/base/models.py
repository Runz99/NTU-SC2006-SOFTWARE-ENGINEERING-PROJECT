from django.db import models

# Create your models here.


class restaurant(models.Model):
    '''
    Restaurant model attributes for storing and accessing in database

    param models.Model: Access django's database API

    '''
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100)
    restaurant_rating = models.CharField(max_length = 100)
    cuisine = models.CharField(max_length = 100)
    lat = models.CharField(max_length = 100)
    lon = models.CharField(max_length = 100)
    opening_hours = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.address

ratingChoice = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),]

class review(models.Model):
    '''
    Review model attributes for storing and accessing in database

    param models.Model: Access django's database API

    '''
    user_name = models.CharField(max_length = 100)
    address = models.ForeignKey(restaurant, on_delete=models.CASCADE)
    restaurant_review = models.CharField(max_length = 100000)
    restaurant_rating = models.CharField(choices = ratingChoice, max_length = 1)

    def __str__(self):
        return self.restaurant_review
