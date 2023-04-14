from base.models import review
from base.forms import reviewForm
from base.models import restaurant
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def leaveReviews(request):
    if(request.session.get('selected_res') == None):
        form = reviewForm(request.POST or None)
    else:
        form = reviewForm(request.POST or None, initial= {'address': request.session['selected_res']['id']})
    
    if request.method == 'POST':
        user_nameV = request.user.username
        form = reviewForm(request.POST) 
        if form.is_valid():
            addressV = form.cleaned_data['address']
            selected_res = restaurant.objects.filter(address = addressV)[0].id
            selected_res = set_selected_res2(selected_res)
            restaurant_reviewV = form.cleaned_data['restaurant_review']
            restaurant_ratingV = form.cleaned_data['restaurant_rating']
            userReview = review(user_name = user_nameV, address = addressV, restaurant_review = restaurant_reviewV, restaurant_rating = restaurant_ratingV)
            userReview.save()
            form = reviewForm()
            updateReviewRating(selected_res)
            messages.success(request, 'Review submission successful! Thank you!')
            return render(request, 'base/leave_reviews.html', {'review' :form})
        else:
            form = reviewForm()  
            return render(request, 'base/leave_reviews.html', {'review' :form})
    return render(request, 'base/leave_reviews.html', {'review' :form})

@login_required(login_url='login')
def view_my_own_reviews(request):
    user_reviews = review.objects.filter(user_name=request.user.username)
    context = {'user_reviews': user_reviews}
    return render(request, 'base/view_my_own_reviews.html', context)

# User can edit or delete their own reviews
@login_required(login_url='login')
def edit_review(request, review_id):
    rev = get_object_or_404(review, id=review_id)
    if request.method == 'POST':
        form = reviewForm(request.POST)
        if form.is_valid():
            rev.address = form.cleaned_data['address']
            selected_res = restaurant.objects.filter(address = rev.address)[0].id
            selected_res = set_selected_res2(selected_res)
            rev.restaurant_review = form.cleaned_data['restaurant_review']
            rev.restaurant_rating = form.cleaned_data['restaurant_rating']
            rev.save()
            updateReviewRating(selected_res)
            return redirect('view_my_own_reviews')
    else:
        initial_data = {
            'address': rev.address,
            'restaurant_review': rev.restaurant_review,
            'restaurant_rating': rev.restaurant_rating,
        }
        form = reviewForm(initial=initial_data)

    return render(request, 'base/edit_review.html', {'form': form})

@login_required(login_url='login')
def delete_review(request, review_id):
    review_instance = get_object_or_404(review, id=review_id, user_name=request.user)
    if request.method == 'POST':
        review_instance.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('view_my_own_reviews')
    
    context = {'review': review_instance}
    return render(request, 'base/delete_review.html', context)

def updateReviewRating(selected_res):
    restaurantReview = review.objects.filter(address = selected_res.get('id'))
    sum = 0
    for reviews in restaurantReview:
        sum+= int(reviews.restaurant_rating) #find total review rating
    if len(restaurantReview) == 0: #if no reviews
        average = 0 #give it a 0
    else:
        average = sum/len(restaurantReview) #get average review rating
        average = str(average)[:4] #set it to 2 dp
    update = restaurant.objects.get(address = selected_res.get('address')) #obtain correct restaurant in database
    update.restaurant_rating = average #update it
    update.save()
    toReturn = []
    toReturn.append(update)
    toReturn.append(restaurantReview)
    toReturn.append(average)
    return toReturn