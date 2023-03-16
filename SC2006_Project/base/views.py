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
