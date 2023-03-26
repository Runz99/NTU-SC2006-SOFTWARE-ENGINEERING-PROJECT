from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import restaurant
from django.views.generic.list import ListView
import requests
import json

def home(request):
    context = {}
    return render(request, 'base/home.html', context)

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
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
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

def findNearestRestaurant(request):
    location_data = None
    res = restaurant.objects.all() #get all restaurant objects in database
    results=None
    if request.GET.get('search'): #get restaurant search
        search = request.GET.get('search')
        results = restaurant.objects.filter(name__contains=search)

    if request.method == "POST":
        ip = requests.get('https://api.ipify.org?format=json')
        ip_data = json.loads(ip.text)
        loc = requests.get("http://ip-api.com/json/"+ip_data["ip"])
        loc_data = loc.text
        location_data = json.loads(loc_data)
        lats = location_data['lat'] #will be used later to calculate distances
        longs = location_data['lon'] #will be used later to calculate distances
    


    context = {'res': res, 'results' : results, 'data': location_data}  #pass res into html
    return render(request, 'base/find_nearest_restaurant.html', context)

def leaveReviews(request):
    context = {}
    return render(request, 'base/leave_reviews.html', context)

def contact(request):
    context = {}
    return render(request, 'base/contact.html',context)

def faq(request):
    context = {}
    return render(request, 'base/faq.html',context)
