from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(restaurant)
class restaurantAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    '''
    Add restaurant model to django's database

    param restaurant: Restaurant model created in models.py
    param ImportExportModelAdmin: Allows import and export function from external files
    param admin.ModelAdmin: Represents model in admin interface

    '''
    list_display = ['name','address','restaurant_rating','cuisine','lat','lon','opening_hours',]

    search_fields = ('name','cuisine')

@admin.register(review)
class reviewAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    '''
    Add review model to django's database

    param review: Review model created in models.py
    param ImportExportModelAdmin: Allows import and export function from external files
    param admin.ModelAdmin: Represents model in admin interface
    
    '''
    list_display = ['user_name', 'address', 'restaurant_review','restaurant_rating']
    search_fields = ('user_name', 'restaurant_rating')

    
