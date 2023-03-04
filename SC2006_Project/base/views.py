from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def home(request):
    context = {}
    return render(request, 'base/home.html', context)

def login(request):
    context = {}
    return render(request, 'base/login.html', context)

def findNearestRestaurant(request):
    context = {}
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
