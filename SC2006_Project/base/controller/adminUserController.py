from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from base.models import review
from django.contrib import messages
from base.forms import *



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