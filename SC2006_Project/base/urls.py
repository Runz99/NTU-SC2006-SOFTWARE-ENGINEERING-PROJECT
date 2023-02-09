from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name='login'),
    path('find-nearest-restaurant/', views.findNearestRestaurant, name='FNR'),
    path('leave-reviews/', views.leaveReviews, name='leaveReview'),
]