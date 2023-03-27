from django import forms
from .models import *
from .models import restaurant


class restaurantDropForm(forms.Form):

    Names = forms.ModelChoiceField(
        queryset=restaurant.objects.values_list("address")
    )