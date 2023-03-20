from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import restaurant

# Register your models here.
#class restaurantAdmin(ImportExportModelAdmin):
#    pass
@admin.register(restaurant)
class restaurantAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','address','restaurant_rating','cuisine','lat','lon','opening_hours',]

    search_fields = ('name','cuisine')


    
