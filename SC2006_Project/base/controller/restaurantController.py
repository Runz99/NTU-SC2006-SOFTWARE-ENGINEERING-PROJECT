from django.shortcuts import render, redirect
import requests
import ast
from .reviewController import updateReviewRating
from .carparkController import get_nearest_carparks
from .findNearbyRestaurantController import calculate_distance
from SC2006_Project.settings import GOOGLE_API_KEY as GOOGLE_API_KEY
API_KEY = GOOGLE_API_KEY

def restaurant_info(request):
    '''
    Gets information of restaurant that user clicked on and renders it in restaurant.html

    param request: Contains information of restaurant clicked
    returns: renders restaurant.html with specified restaurant's info and restaurant's reviews

    '''
    
    selected_res = request.session.get('selected_res')
    cuisineList = [n.strip() for n in ast.literal_eval(selected_res['cuisine'])]
    #chosen_res = restaurant.objects.get(id = res_id)

    update = updateReviewRating(selected_res)
    selected_res = update[0] #get updated restaurant entry to display
    restaurantReview = update[1]
    
    nearest_carparks = get_nearest_carparks(selected_res.lat, selected_res.lon, API_KEY)
    for carpark in nearest_carparks:
        carpark['distance'] = calculate_distance(float(selected_res.lat), float(selected_res.lon), float(carpark['geometry']['location']['lat']), float(carpark['geometry']['location']['lng']))

    nearest_carparks.sort(key=lambda carpark: carpark['distance'])  # Sort by distance
    nearest_carparks = nearest_carparks[:5]  # Get the top 5 nearest carparks
    

    context = {'selected_res': selected_res, 
               'restaurantReview': restaurantReview, 
               'nearest_carparks': nearest_carparks,
               'cuisineList': cuisineList}
    

    return render(request, 'base/restaurantUI/restaurant.html', context)