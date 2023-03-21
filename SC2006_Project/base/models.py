from django.db import models

# Create your models here.
class restaurant(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100)
    restaurant_rating = models.CharField(max_length = 100)
    cuisine = models.CharField(max_length = 100)
    lat = models.CharField(max_length = 100)
    lon = models.CharField(max_length = 100)
    opening_hours = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.address
    
class review(models.Model):
    userName = models.CharField(max_length = 100)
    restaurantName = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100)
    restaurant_rating = models.CharField(max_length = 2)
    restaurant_review = models.CharField(max_length = 100000)

    def __str__(self):
        return self.restaurant_review
