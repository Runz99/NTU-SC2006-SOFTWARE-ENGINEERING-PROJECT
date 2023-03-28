from django import forms
from .models import *
from .models import restaurant
from .models import review

ratingChoice = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),]


class reviewForm(forms.Form):
    #user_name = forms.CharField(max_length = 100)
    address = forms.ModelChoiceField(
            queryset=restaurant.objects.all().order_by("address"),
            label = "Restaurant Name"
            )
    restaurant_review = forms.CharField(label = "Review Text", max_length=100000)
    restaurant_rating = forms.CharField(label = "Rating", widget=forms.Select(choices=ratingChoice))
    
    