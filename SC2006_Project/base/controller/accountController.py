from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required(login_url='login')
def account(request):
    is_admin = request.user.is_staff
    return render(request, 'base/accountUI/account.html', {'is_admin': is_admin})