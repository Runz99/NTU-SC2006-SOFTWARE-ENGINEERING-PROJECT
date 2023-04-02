from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.db import models
from .models import restaurant
from .models import review
from django.views.generic.list import ListView
from django.views.generic import CreateView
from .forms import *
from .forms import reviewForm
from .forms import CoordinatesForm
import requests
import json
import math

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

def findNearestRestaurant(request):
    location_data = None
    form = None
    user_lats = None
    user_longs = None
    top_10_res = None
    res = restaurant.objects.all() #get all restaurant objects in database
    results=None
    form = CoordinatesForm()
    if request.GET.get('search'): #get restaurant search
        search = request.GET.get('search')
        results = restaurant.objects.filter(name__contains=search)

    if request.method == "POST":
        # ip = requests.get('https://api.ipify.org?format=json')
        # ip_data = json.loads(ip.text)
        # loc = requests.get("http://ip-api.com/json/"+ip_data["ip"])
        # loc_data = loc.text
        # location_data = json.loads(loc_data)
        form = CoordinatesForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['use_current_location']:
                # current_location = getCurrentLocation()
                # form.cleaned_data['user_lats'] = current_location['latitude']
                # form.cleaned_data['user_longs'] = current_location['longitude']
                return render(request, 'base/find_nearest_restaurant.html', {'form': form, 'get_current_location': True})
            else:
                user_lats = form.cleaned_data['user_lats'] #will be used later to calculate distances
                user_longs = form.cleaned_data['user_longs'] #will be used later to calculate distances
        # Calculate distance between user and each place
        for eat in res:
            eat.distance = calculate_distance(user_lats, user_longs, float(eat.lat), float(eat.lon))
        # Sort places by distance
        sorted_res = sorted(res, key=lambda eat: eat.distance)

        top_10_res = sorted_res[:10]
        
    
    context = {'res': res, 'results' : results, 'form': form, 'lists':top_10_res}  #pass res into html
    return render(request, 'base/find_nearest_restaurant.html', context)

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

    selected_res = request.session.get('selected_res')
    #chosen_res = restaurant.objects.get(id = res_id)
    restaurantReview = review.objects.filter(address = selected_res.get('id'))

    context = {'selected_res': selected_res, 'restaurantReview' : restaurantReview}
    return render(request, 'base/restaurant.html', context)


#===========================================================================================================================================================

def contact(request):
    context = {}
    return render(request, 'base/contact.html',context)

def faq(request):
    context = {}
    return render(request, 'base/faq.html',context)
