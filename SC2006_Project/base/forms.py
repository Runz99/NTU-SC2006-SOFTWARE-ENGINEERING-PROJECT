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
    username = forms.CharField(label ="User Name", max_length=30, required=True, error_messages={'required': 'Username is required.'})
    first_name = forms.CharField(label ="First Name", max_length=30, required=True, error_messages={'required': 'First name is required.'})
    last_name = forms.CharField(label ="Last Name", max_length=30, required=True, error_messages={'required': 'Last name is required.'})
    email = forms.EmailField(label ="Email", max_length=254, required=True, error_messages={'required': 'Email is required.', 'invalid': 'Enter a valid email address.'})
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label

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



