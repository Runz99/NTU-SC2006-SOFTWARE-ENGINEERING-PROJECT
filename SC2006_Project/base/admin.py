from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *

# Register your models here.
#class restaurantAdmin(ImportExportModelAdmin):
#    pass
@admin.register(restaurant)
class restaurantAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','address','restaurant_rating','cuisine','lat','lon','opening_hours',]

    search_fields = ('name','cuisine')

@admin.register(review)
class reviewAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['user_name', 'address', 'restaurant_review','restaurant_rating']
    search_fields = ('user_name', 'restaurant_rating')

    
