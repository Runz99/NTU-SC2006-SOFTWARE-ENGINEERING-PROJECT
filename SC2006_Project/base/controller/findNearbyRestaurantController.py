from django.shortcuts import render, redirect
from base.models import restaurant
import requests
import urllib.parse
import math
from SC2006_Project.settings import GOOGLE_API_KEY as GOOGLE_API_KEY
API_KEY = GOOGLE_API_KEY
import ast
from .reviewController import updateReviewRating
from .setSelectedResHelper import *

#===========================================================================================================================================================
# function that takes in user location and saves it, redirect to filter page (find_nearest_restaurant_1)
def find_nearest_restaurant_1(request):
    location_data = None
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
    
    context = {'data': location_data}  #pass res into html
    return render(request, 'base/find_nearest_restaurant_1.html', context)


#===========================================================================================================================================================
# function that takes in user's cuisine preferences, which is optional (find_nearest_restaurant_2)
import random
def find_nearest_restaurant_2(request):
    userLats = request.session['user_lats']
    userLongs =request.session['user_longs']
    userLatsStr = str(userLats)
    userLongsStr = str(userLongs)
    filteredRestaurantList = []
    cuisineList = []
    restrictionList = []
    maxDist = 0
    minRating = 0
    newform = True
    currentLocation = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+userLatsStr+","+userLongsStr+"&key="+API_KEY)
    currentLocationStr = currentLocation.json()['results'][0]['formatted_address']
    mapMarkersList = []

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
            'minRating': minRating
        }

    if request.method == "POST":
        #cuisine_choices = restaurant.objects.values_list('cuisine',flat=True)
        cuisineList = request.POST.getlist('cuisines')
        restrictionList = request.POST.getlist('restrictions')
        maxDist = request.POST.get('distance')
        minRating = request.POST.get('minRating')
        newform = False
        for eat in sortedRestaurantList:
            eatTags = [n.strip() for n in ast.literal_eval(eat.cuisine)]
            # print("eattags: "+ str(eatTags))
            if(set(restrictionList).issubset(set(eatTags))):  #meets all restrictions
                # print("restriction list: "+ str(restrictionList))
                if(len(set(eatTags).intersection(set(cuisineList))) != 0): #meets at least one cuisine
                    # print("cuisine list: "+ str(cuisineList))
                    if(float(eat.distance) <= float(maxDist)): #within max distance
                         currentRating = updateReviewRating(set_selected_res2(eat.id))[2]
                         if float(currentRating) >= float(minRating):
                            filteredRestaurantList.append({"id": eat.id,
                                                        "name": eat.name,
                                                        "lat": eat.lat, 
                                                        "lon": eat.lon,
                                                        "distance": eat.distance,
                                                        "cuisine": ", ".join(eatTags),
                                                        "rating": currentRating,
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
                'minRating': minRating
            }
        if request.POST.get('action') == 'randomise':
            if len(filteredRestaurantList) == 0:
                return 0
            else:
                chosenRestaurant = random.choice(filteredRestaurantList)
                return redirect('set_selected_res', res_id=chosenRestaurant['id'])

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

