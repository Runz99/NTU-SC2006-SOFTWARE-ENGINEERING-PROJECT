from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from base.forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash



@login_required(login_url='login')
def change_particulars(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('account')
        else:
            messages.error(request, 'Error updating profile.')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'base/settingsUI/change_particulars.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change
            messages.success(request, 'Password changed successfully. Please log in again.')
            return redirect('login')
        else:
            messages.error(request, 'Error updating password.')
    else:
        password_form = CustomPasswordChangeForm(request.user)

    context = {'password_form': password_form}
    return render(request, 'base/settingsUI/change_password.html', context)


