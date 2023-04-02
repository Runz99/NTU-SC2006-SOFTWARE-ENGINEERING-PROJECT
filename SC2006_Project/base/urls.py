from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import set_selected_res, restaurant_info

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('create-user/', views.createUser, name='create_user'),
    path('find-nearest-restaurant/', views.findNearestRestaurant, name='FNR'),
    path('leave-reviews/', views.leaveReviews, name='leaveReview'),
    path('contact/', views.contact, name = 'contact'),
    path('faq/', views.faq, name = 'faq'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('set-selected-place/<int:res_id>/', views.set_selected_res, name='set_selected_res'),
    path('restaurant-info', restaurant_info, name='restaurant_info'),
    #path('restaurant-info/<int:place_id>/', restaurant_info, name='restaurant_info'),

]