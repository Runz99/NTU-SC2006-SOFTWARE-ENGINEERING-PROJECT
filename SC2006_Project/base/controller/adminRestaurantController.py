from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from base.models import restaurant
from django.shortcuts import get_object_or_404
from django.contrib import messages
from base.forms import *


@user_passes_test(lambda u: u.is_staff, login_url='login')
def list_restaurants(request):
    restaurants = restaurant.objects.all()
    return render(request, 'base/adminRestaurantUI/list_restaurants.html', {'restaurants': restaurants})

@user_passes_test(lambda u: u.is_staff, login_url='login')
def delete_restaurant(request, restaurant_id):
    restaurant_instance = get_object_or_404(restaurant, id=restaurant_id)
    if request.method == 'POST':
        restaurant_instance.delete()
        messages.success(request, 'Restaurant deleted successfully!')
        return redirect('list_restaurants')
    context = {'restaurant': restaurant_instance}
    return render(request, 'base/adminRestaurantUI/delete_restaurant.html', context)

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
    return render(request, 'base/adminRestaurantUI/add_restaurant.html', {'form': form})