from django import forms
from .models import *
from .models import restaurant
from .models import review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm

ratingChoice = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),]


class reviewForm(forms.Form):
    '''
    Review form to store and access user created reviews in database

    param models.Model: Access django's form functionalities

    '''
    address = forms.ModelChoiceField(
            queryset=restaurant.objects.all().order_by("address"),
            label = "Restaurant Name"
            )
    restaurant_review = forms.CharField(label = "Review Text", max_length=100000)
    restaurant_rating = forms.CharField(label = "Rating", widget=forms.Select(choices=ratingChoice))
    
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')    

class CoordinatesForm(forms.Form):
    user_lats = forms.FloatField()
    user_longs = forms.FloatField()
    use_current_location = forms.BooleanField(required=False, label='use_current_location')

class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class CustomPasswordChangeForm(PasswordChangeForm):
    
    pass

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = restaurant
        fields = '__all__'



