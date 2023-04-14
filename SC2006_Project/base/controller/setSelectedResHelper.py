from django.shortcuts import render, redirect
from base.models import restaurant

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

def set_selected_res2(res_id):
    selected_res = restaurant.objects.get(id=res_id)

    selected_res = {
        'id': selected_res.id,
        'name': selected_res.name,
        'address': selected_res.address,
        'restaurant_rating' : selected_res.restaurant_rating,
        'lat': selected_res.lat,
        'lon': selected_res.lon,
        'cuisine': selected_res.cuisine
    }

    return selected_res