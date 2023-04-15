from django.shortcuts import render, redirect
from base.models import restaurant

def searchRestaurant(request):
    res = restaurant.objects.all() #get all restaurant objects in database
    results=None

    if request.GET.get('search'): #get restaurant search
        search = request.GET.get('search')
        results = restaurant.objects.filter(address__contains=search)
    context = {'res': res, 'results' : results}  #pass res into html
    return render(request, 'base/searchUI/search_restaurant.html', context)