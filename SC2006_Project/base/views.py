from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .forms import CustomUserCreationForm
from django.db import models
from .models import restaurant
from .models import review
from django.views.generic.list import ListView
from django.views.generic import CreateView
from .forms import *
from .forms import reviewForm
import requests
import googlemaps
import json
import math
import urllib.parse
import os

#API_KEY = os.environ.get('API_KEY')
#==========================================================================================================================================================

def home(request):
    context = {}
    return render(request, 'base/home.html', context)

#==========================================================================================================================================================

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Account does not exist")
            
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #return redirect('home')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'base/login.html', context)

def logOut(request):
    logout(request)
    return redirect('home')

def createUser(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "an error has occured during registration")
    context = {'form':form}
    return render(request, 'base/create_user.html', context)

#===========================================================================================================================================================

def searchRestaurant(request):
    res = restaurant.objects.all() #get all restaurant objects in database
    results=None

    if request.GET.get('search'): #get restaurant search
        search = request.GET.get('search')
        results = restaurant.objects.filter(name__contains=search)
    context = {'res': res, 'results' : results}  #pass res into html
    return render(request, 'base/search_restaurant.html', context)

# function that takes in user location and saves it, redirect to filter page (find_nearest_restaurant_2)
def find_nearest_restaurant_1(request):
    location_data = None
    top_10_res = None
    res = restaurant.objects.all() #get all restaurant objects in database
    user_lats = None
    user_longs = None

    if request.GET.get('userAddress'):
        userAddress = request.GET.get('userAddress')
        #calls google API to get user's location:
        encUA = urllib.parse.quote(userAddress)
        API_KEY = settings.GOOGLE_API_KEY
        result = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+encUA+"&key="+API_KEY)
        location_data = result.json()
        user_lats = location_data['results'][0]['geometry']['location']['lat']
        user_longs = location_data['results'][0]['geometry']['location']['lng'] 

        request.session['user_lats'] = user_lats
        request.session['user_longs'] = user_longs
        return redirect('find_nearest_restaurant_2')


    if request.method == "POST":
        user_lats = float(request.POST.get('latitude'))
        user_longs = float(request.POST.get('longitude')) #will be used later to calculate distances

        request.session['user_lats'] = user_lats
        request.session['user_longs'] = user_longs
        return redirect('find_nearest_restaurant_2')
    
    context = {'res': res,'data': location_data}  #pass res into html
    return render(request, 'base/find_nearest_restaurant_1.html', context)

# function that takes in user's cuisine preferences, which is optional (find_nearest_restaurant_3)
def find_nearest_restaurant_2(request):
    #cuisine_choices = restaurant.objects.values_list('cuisine',flat=True)
    if request.method == "POST":
        #cuisine_choices = restaurant.objects.values_list('cuisine',flat=True)
        selected_choice = request.POST.get('cuisine_dropdown')
        if selected_choice:
            request.session['selected_choice'] = selected_choice
        #request.session['selected_choice'] = selected_choice
        return redirect('find_nearest_restaurant_3')

    else:
        cuisine_choices = restaurant.objects.values_list('cuisine',flat=True)
        print(cuisine_choices)
        context = {'cuisine_choice':cuisine_choices}
        return render(request, 'base/find_nearest_restaurant_2.html', context)

# function that displays results from previous 2 parameters
def find_nearest_restaurant_3(request):
    res = restaurant.objects.all()
    user_lats = request.session.get('user_lats')
    user_longs = request.session.get('user_longs')
    top_10_res = None

    for eat in res:
        eat.distance = calculate_distance(user_lats, user_longs, float(eat.lat), float(eat.lon))
        # Sort places by distance
    sorted_res = sorted(res, key=lambda eat: eat.distance)
    top_10_res = sorted_res[:10]
    
    #context = {'res': res, 'results' : results, 'data': location_data, 'lists':top_10_res} 
    context = {'res': res, 'lists':top_10_res}  #pass res into html
    return render(request, 'base/find_nearest_restaurant_3.html', context)


    
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in km
    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c  # Distance in km
    return distance

def set_selected_res(request, res_id):
    selected_res = restaurant.objects.get(id=res_id)

    request.session['selected_res'] = {
        'id': selected_res.id,
        'name': selected_res.name,
        'address': selected_res.address,
        'lat': selected_res.lat,
        'lon': selected_res.lon,
        'cuisine': selected_res.cuisine
    }

    return redirect('restaurant_info')

#===========================================================================================================================================================

@login_required(login_url='login')
def leaveReviews(request):
    form = reviewForm(request.POST or None)
    
    if request.method == 'POST':
        user_nameV = request.user.username
        form = reviewForm(request.POST) 
        if form.is_valid():
            addressV = form.cleaned_data['address']
            restaurant_reviewV = form.cleaned_data['restaurant_review']
            restaurant_ratingV = form.cleaned_data['restaurant_rating']
            userReview = review(user_name = user_nameV, address = addressV, restaurant_review = restaurant_reviewV, restaurant_rating = restaurant_ratingV)
            userReview.save()
            form = reviewForm()
            messages.success(request, 'Review submission successful! Thank you!')
            return render(request, 'base/leave_reviews.html', {'review' :form})
        else:
            form = reviewForm()  
            return render(request, 'base/leave_reviews.html', {'review' :form})
    return render(request, 'base/leave_reviews.html', {'review' :form})

#===========================================================================================================================================================

def restaurant_info(request):
    '''
    Gets information of restaurant that user clicked on and renders it in restaurant.html

    param request: Contains information of restaurant clicked
    returns: renders restaurant.html with specified restaurant's info and restaurant's reviews

    '''
    selected_res = request.session.get('selected_res')
    #chosen_res = restaurant.objects.get(id = res_id)
    restaurantReview = review.objects.filter(address = selected_res.get('id'))

    context = {'selected_res': selected_res, 'restaurantReview' : restaurantReview}
    return render(request, 'base/restaurant.html', context)


#===========================================================================================================================================================

def contact(request):
    '''
    Renders contact.html when contact is clicked

    param request: Passes state through system
    returns: renders contact.html

    '''
    context = {}
    return render(request, 'base/contact.html',context)

def faq(request):
    '''
    Renders faq.html when contact is clicked

    param request: Passes state through system
    returns: renders faq.html

    '''
    context = {}
    return render(request, 'base/faq.html',context)
