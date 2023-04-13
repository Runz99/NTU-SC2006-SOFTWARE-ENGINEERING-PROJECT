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
from django.contrib.auth.forms import UserChangeForm
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
import ast
import random
API_KEY = settings.GOOGLE_API_KEY


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

#===========================================================================================================================================================
# function that takes in user location and saves it, redirect to filter page (find_nearest_restaurant_2)
def find_nearest_restaurant_1(request):
    location_data = None
    res = restaurant.objects.all() #get all restaurant objects in database
    user_lats = None
    user_longs = None

    if request.GET.get('userAddress'):
        userAddress = request.GET.get('userAddress')
        #calls google API to get user's location:
        encUA = urllib.parse.quote(userAddress)
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


#===========================================================================================================================================================
# function that takes in user's cuisine preferences, which is optional (find_nearest_restaurant_3)
def find_nearest_restaurant_2(request):
    userLats = request.session['user_lats']
    userLongs =request.session['user_longs']
    userLatsStr = str(userLats)
    userLongsStr = str(userLongs)
    filteredRestaurantList = []
    cuisineList = []
    restrictionList = []
    maxDist = 0
    newform = True
    currentLocation = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+userLatsStr+","+userLongsStr+"&key="+API_KEY)
    currentLocationStr = currentLocation.json()['results'][0]['formatted_address']

    res = restaurant.objects.all()
    resultRestaurantList = []
    for eat in res:
        eat.distance = calculate_distance(userLats, userLongs, float(eat.lat), float(eat.lon))
        # Sort places by distance
        if eat.distance <= 5:
            resultRestaurantList.append(eat)
    sortedRestaurantList = sorted(resultRestaurantList, key= lambda eat: eat.distance)

    cuisine_options = ["Alcohol", "Bubble Tea", "Chinese", "Coffee & Tea", 
                       "Dessert", "Fast Food", "Ice Cream", "Indian", "Indonesian", 
                       "Italian", "Japanese", "Korean", "Local","Malaysian", "Pasta",
                       "Taiwanese","Thai","Seafood","Steak","Western"]
    
    restriction_options = ["Halal", "Vegetarian Friendly", "Vegan"]
    context = {
            'currentLocationStr':currentLocationStr, 
            'userLats':userLatsStr, 
            'userLongs':userLongsStr, 'API_KEY': API_KEY,
            'cuisine_options':cuisine_options,
            'restriction_options':restriction_options,
            'newform':newform,
            'maxDist': maxDist,
            'restrictionList':restrictionList,
            'cuisineList': cuisineList,
        }

    if request.method == "POST":
        #cuisine_choices = restaurant.objects.values_list('cuisine',flat=True)
        cuisineList = request.POST.getlist('cuisines')
        restrictionList = request.POST.getlist('restrictions')
        maxDist = request.POST.get('distance')
        newform = False
        for eat in sortedRestaurantList:
            eatTags = [n.strip() for n in ast.literal_eval(eat.cuisine)]
            # print("eattags: "+ str(eatTags))
            if(set(restrictionList).issubset(set(eatTags))):  #meets all restrictions
                # print("restriction list: "+ str(restrictionList))
                if(len(set(eatTags).intersection(set(cuisineList))) != 0): #meets at least one cuisine
                    # print("cuisine list: "+ str(cuisineList))
                    if(eat.distance <= float(maxDist)): #within max distance
                        filteredRestaurantList.append({"id": eat.id,
                                                    "name": eat.name,
                                                    "lat": eat.lat, 
                                                    "lon": eat.lon,
                                                    "distance": eat.distance,
                                                    "cuisine": ", ".join(eatTags)
                                                    })
                        # print(eat.distance, maxDist)

        context = {
                'maxDist': maxDist,
                'restrictionList':restrictionList,
                'cuisineList': cuisineList,
                'newform':newform, 
                'currentLocationStr':currentLocationStr, 
                'userLats':userLatsStr, 
                'userLongs':userLongsStr, 
                'API_KEY': API_KEY, 
                'filteredRestaurantList':filteredRestaurantList,
                'cuisine_options':cuisine_options,
                'restriction_options':restriction_options,
            }
        if request.POST.get('action') == 'randomise':
            if len(filteredRestaurantList) == 0:
                messages.error(request, 'No restaurants found!')
            else:
                chosenRestaurant = random.choice(filteredRestaurantList)
                return redirect('set_selected_res', res_id=chosenRestaurant.id)

    return render(request, 'base/find_nearest_restaurant_2.html', context)

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
#===========================================================================================================================================================
def set_selected_res(request, res_id):
    selected_res = restaurant.objects.get(id=res_id)

    request.session['selected_res'] = {
        'id': selected_res.id,
        'name': selected_res.name,
        'address': selected_res.address,
        'restaurant_rating' : selected_res.restaurant_rating,
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


#===========================================================================================================================================================
# User Account Page 
@login_required(login_url='login')
def account(request):
    is_admin = request.user.is_staff
    return render(request, 'base/account.html', {'is_admin': is_admin})

# View users' own reviews 
@login_required(login_url='login')
def view_my_own_reviews(request):
    user_reviews = review.objects.filter(user_name=request.user.username)
    context = {'user_reviews': user_reviews}
    return render(request, 'base/view_my_own_reviews.html', context)

# User can edit or delete their own reviews
@login_required(login_url='login')
def edit_review(request, review_id):
    rev = get_object_or_404(review, id=review_id)
    if request.method == 'POST':
        form = reviewForm(request.POST)
        if form.is_valid():
            rev.address = form.cleaned_data['address']
            rev.restaurant_review = form.cleaned_data['restaurant_review']
            rev.restaurant_rating = form.cleaned_data['restaurant_rating']
            rev.save()
            return redirect('view_my_own_reviews')
    else:
        initial_data = {
            'address': rev.address,
            'restaurant_review': rev.restaurant_review,
            'restaurant_rating': rev.restaurant_rating,
        }
        form = reviewForm(initial=initial_data)

    return render(request, 'base/edit_review.html', {'form': form})

@login_required(login_url='login')
def delete_review(request, review_id):
    review_instance = get_object_or_404(review, id=review_id, user_name=request.user)
    if request.method == 'POST':
        review_instance.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('view_my_own_reviews')
    
    context = {'review': review_instance}
    return render(request, 'base/delete_review.html', context)

# Change users' particulars
@login_required(login_url='login')
def change_particulars(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('account')
        else:
            messages.error(request, 'Error updating profile.')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'base/change_particulars.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change
            messages.success(request, 'Password changed successfully. Please log in again.')
            return redirect('login')
        else:
            messages.error(request, 'Error updating password.')
    else:
        password_form = CustomPasswordChangeForm(request.user)

    context = {'password_form': password_form}
    return render(request, 'base/change_password.html', context)

# For admin account to manage users and restaurants
@user_passes_test(lambda u: u.is_staff, login_url='login')
def list_users(request):
    users = User.objects.all()
    return render(request, 'base/list_users.html', {'users': users})

@user_passes_test(lambda u: u.is_staff, login_url='login')
def delete_users(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('list_users')

@user_passes_test(lambda u: u.is_staff, login_url='login')
def delete_reviews(request, user_id):
    if request.method == "POST":
        review_ids = request.POST.getlist('review_ids')
        for review_id in review_ids:
            review.objects.filter(pk=review_id).delete()
        return redirect('list_users')

    user = User.objects.get(pk=user_id)
    reviews = review.objects.filter(user_name=user)  # Use user_name field to filter reviews
    return render(request, 'base/delete_reviews.html', {'reviews': reviews, 'user_id': user_id})


@user_passes_test(lambda u: u.is_staff, login_url='login')
def update_user_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated user {user.username} account particulars.")
            return EditProfileForm(reverse('list_users'))
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'base/update_user_account.html', {'form': form, 'user_id': user_id})

@user_passes_test(lambda u: u.is_staff, login_url='login')
def list_restaurants(request):
    restaurants = restaurant.objects.all()
    return render(request, 'base/list_restaurants.html', {'restaurants': restaurants})

@user_passes_test(lambda u: u.is_staff, login_url='login')
def delete_restaurant(request, restaurant_id):
    restaurant_instance = get_object_or_404(restaurant, id=restaurant_id)
    if request.method == 'POST':
        restaurant_instance.delete()
        messages.success(request, 'Restaurant deleted successfully!')
        return redirect('list_restaurants')
    context = {'restaurant': restaurant_instance}
    return render(request, 'base/delete_restaurant.html', context)

@user_passes_test(lambda u: u.is_staff, login_url='login')
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant added successfully!')
            return redirect('list_restaurants')
    else:
        form = RestaurantForm()
    return render(request, 'base/add_restaurant.html', {'form': form})



#===========================================================================================================================================================

import requests
import json

ONEMAP_API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEwMTgxLCJ1c2VyX2lkIjoxMDE4MSwiZW1haWwiOiJ4dWp1bnpoZTAxMTNAb3V0bG9vay5jb20iLCJmb3JldmVyIjpmYWxzZSwiaXNzIjoiaHR0cDpcL1wvb20yLmRmZS5vbmVtYXAuc2dcL2FwaVwvdjJcL3VzZXJcL3Nlc3Npb24iLCJpYXQiOjE2ODEzMjA2ODIsImV4cCI6MTY4MTc1MjY4MiwibmJmIjoxNjgxMzIwNjgyLCJqdGkiOiIyNzY2MmZjNGMxNDE0NWVkYjA0MmUzYjcxYzYyYzdjNiJ9.3KvTDjidt7hNxb4hD-JmYvcY3I1eOYsL5zMfD59OGqY'

def restaurant_info(request):
    '''
    Gets information of restaurant that user clicked on and renders it in restaurant.html

    param request: Contains information of restaurant clicked
    returns: renders restaurant.html with specified restaurant's info and restaurant's reviews

    '''
    selected_res = request.session.get('selected_res')
    #chosen_res = restaurant.objects.get(id = res_id)
    restaurantReview = review.objects.filter(address = selected_res.get('id'))
    sum = 0
    for reviews in restaurantReview:
        sum+= int(reviews.restaurant_rating) #find total review rating
    if len(restaurantReview) == 0: #if no reviews
        average = 0 #give it a 0
    else:
        average = sum/len(restaurantReview) #get average review rating
        average = str(average)[:4] #set it to 2 dp
    update = restaurant.objects.get(address = selected_res.get('address')) #obtain correct restaurant in database
    update.restaurant_rating = average #update it
    update.save()
    selected_res = update #get updated restaurant entry to display
    
    nearest_carparks = get_nearest_carparks(selected_res.lat, selected_res.lon, ONEMAP_API_KEY)
    for carpark in nearest_carparks:
        carpark['distance'] = calculate_distance(float(selected_res.lat), float(selected_res.lon), float(carpark['LATITUDE']), float(carpark['LONGITUDE']))

    context = {'selected_res': selected_res, 'restaurantReview': restaurantReview, 'nearest_carparks': nearest_carparks}
    return render(request, 'base/restaurant.html', context)

def get_nearest_carparks(lat, lon, api_key):
    try:
        base_url = "https://developers.onemap.sg/commonapi/search?"
        query = f"searchVal=Car%20Park&returnGeom=Y&getAddrDetails=Y&pageNum=1"
        url = f"{base_url}{query}&lat={lat}&lng={lon}&APIKey={api_key}"
        response = requests.get(url)
        data = response.json()

        if data['found'] > 0:
            nearest_carparks = data['results'][:5]  # Get the top 5 nearest carparks
            return nearest_carparks
        
        else:
            return []

    except json.JSONDecodeError:
        print("Error parsing JSON response from OneMap API")
        return []
    except Exception as e:
        print("Error occurred while fetching nearest carparks:", e)
        return []



