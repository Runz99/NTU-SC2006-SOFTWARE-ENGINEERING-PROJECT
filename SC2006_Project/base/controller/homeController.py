from django.shortcuts import render, redirect
def home(request):
    context = {}
    return render(request, 'base/homeUI/home.html', context)