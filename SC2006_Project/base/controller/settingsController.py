from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from base.forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from base.models import review
from base.models import restaurant


@login_required(login_url='login')
def account(request):
    is_admin = request.user.is_staff
    return render(request, 'base/account.html', {'is_admin': is_admin})

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
    return render(request, 'base/change_particulars.html', context)

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
    return render(request, 'base/change_password.html', context)

# For admin account to manage users and restaurants
@user_passes_test(lambda u: u.is_staff, login_url='login')
def list_users(request):
    users = User.objects.all()
    return render(request, 'base/list_users.html', {'users': users})

@user_passes_test(lambda u: u.is_staff, login_url='login')
def delete_users(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('list_users')

@user_passes_test(lambda u: u.is_staff, login_url='login')
def delete_reviews(request, user_id):
    if request.method == "POST":
        review_ids = request.POST.getlist('review_ids')
        for review_id in review_ids:
            review.objects.filter(pk=review_id).delete()
        return redirect('list_users')

    user = User.objects.get(pk=user_id)
    reviews = review.objects.filter(user_name=user)  # Use user_name field to filter reviews
    return render(request, 'base/delete_reviews.html', {'reviews': reviews, 'user_id': user_id})


@user_passes_test(lambda u: u.is_staff, login_url='login')
def update_user_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated user {user.username} account particulars.")
            return EditProfileForm(reverse('list_users'))
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'base/update_user_account.html', {'form': form, 'user_id': user_id})

@user_passes_test(lambda u: u.is_staff, login_url='login')
def list_restaurants(request):
    restaurants = restaurant.objects.all()
    return render(request, 'base/list_restaurants.html', {'restaurants': restaurants})

@user_passes_test(lambda u: u.is_staff, login_url='login')
def delete_restaurant(request, restaurant_id):
    restaurant_instance = get_object_or_404(restaurant, id=restaurant_id)
    if request.method == 'POST':
        restaurant_instance.delete()
        messages.success(request, 'Restaurant deleted successfully!')
        return redirect('list_restaurants')
    context = {'restaurant': restaurant_instance}
    return render(request, 'base/delete_restaurant.html', context)

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
    return render(request, 'base/add_restaurant.html', {'form': form})