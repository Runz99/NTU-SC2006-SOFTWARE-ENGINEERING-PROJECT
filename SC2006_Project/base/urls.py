from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('create-user/', views.createUser, name='create_user'),
    path('find-nearest-restaurant/', views.findNearestRestaurant, name='FNR'),
    path('restaurant/', views.restaurant_info, name = 'restaurant_info'),
    path('leave-reviews/', views.leaveReviews, name='leaveReview'),
    path('contact/', views.contact, name = 'contact'),
    path('faq/', views.faq, name = 'faq')

]