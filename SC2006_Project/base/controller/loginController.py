from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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