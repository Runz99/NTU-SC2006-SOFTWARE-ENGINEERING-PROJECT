from django.urls import path
from django.contrib.auth import views as auth_views
from . import controller
from .controller import *

urlpatterns = [
    path('', controller.home, name="home"),
    path('login/', controller.loginPage, name='login'),
    path('logout/', controller.logOut, name='logout'),
    path('create-user/', controller.createUser, name='create_user'),
    path('search-restaurant/', controller.searchRestaurant, name='search_restaurant'),
    path('leave-reviews/', controller.leaveReviews, name='leaveReview'),
    path('contact/', controller.contact, name = 'contact'),
    path('faq/',controller.faq, name = 'faq'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('set-selected-place/<int:res_id>/', controller.set_selected_res, name='set_selected_res'),
    path('restaurant-info', restaurant_info, name='restaurant_info'),
    path('find-nearest-restaurant', controller.find_nearest_restaurant_1, name='find_nearest_restaurant_1'),
    path('find-nearest-restaurant-2', controller.find_nearest_restaurant_2, name='find_nearest_restaurant_2'),
    # path('find-nearest-restaurant-3', views.find_nearest_restaurant_3, name='find_nearest_restaurant_3'),
    #path('restaurant-info/<int:place_id>/', restaurant_info, name='restaurant_info'),
    path('account', controller.account, name='account'),
    path('change_particulars/', controller.change_particulars, name='change_particulars'),
    path('view_my_own_reviews/', controller.view_my_own_reviews, name='view_my_own_reviews'),
    path('edit_review/<int:review_id>/', controller.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', controller.delete_review, name='delete_review'),
    path('delete_users/<int:user_id>/', controller.delete_users, name='delete_users'),
    path('delete_reviews/<int:user_id>/', controller.delete_reviews, name='delete_reviews'),
    path('update_user_account/<int:user_id>/', controller.update_user_account, name='update_user_account'),
    path('list_users/', controller.list_users, name='list_users'),
    path('list_restaurants/', controller.list_restaurants, name='list_restaurants'),
    path('delete_restaurant/<int:restaurant_id>/', controller.delete_restaurant, name='delete_restaurant'),
    path('add_restaurant/', controller.add_restaurant, name='add_restaurant'),
    path('change_password/', controller.change_password, name='change_password'),
    path('accounts/login/', controller.loginPage, name='login'),
]