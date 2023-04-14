from django.shortcuts import render, redirect
from django.contrib import messages
from base.forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout

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
