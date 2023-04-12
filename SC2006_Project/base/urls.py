from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import set_selected_res, restaurant_info

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('create-user/', views.createUser, name='create_user'),
    path('search-restaurant/', views.searchRestaurant, name='search_restaurant'),
    path('leave-reviews/', views.leaveReviews, name='leaveReview'),
    path('contact/', views.contact, name = 'contact'),
    path('faq/', views.faq, name = 'faq'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('set-selected-place/<int:res_id>/', views.set_selected_res, name='set_selected_res'),
    path('restaurant-info', restaurant_info, name='restaurant_info'),
    path('find-nearest-restaurant', views.find_nearest_restaurant_1, name='find_nearest_restaurant_1'),
    path('find-nearest-restaurant-2', views.find_nearest_restaurant_2, name='find_nearest_restaurant_2'),
    # path('find-nearest-restaurant-3', views.find_nearest_restaurant_3, name='find_nearest_restaurant_3'),
    #path('restaurant-info/<int:place_id>/', restaurant_info, name='restaurant_info'),
    path('account', views.account, name='account'),
    path('change_particulars/', views.change_particulars, name='change_particulars'),
    path('view_my_own_reviews/', views.view_my_own_reviews, name='view_my_own_reviews'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('delete_users/<int:user_id>/', views.delete_users, name='delete_users'),
    path('delete_reviews/<int:user_id>/', views.delete_reviews, name='delete_reviews'),
    path('update_user_account/<int:user_id>/', views.update_user_account, name='update_user_account'),
    path('list_users/', views.list_users, name='list_users'),
    path('list_restaurants/', views.list_restaurants, name='list_restaurants'),
    path('delete_restaurant/<int:restaurant_id>/', views.delete_restaurant, name='delete_restaurant'),
    path('add_restaurant/', views.add_restaurant, name='add_restaurant'),
    path('change_password/', views.change_password, name='change_password'),
]