from django.contrib import admin

from .models import Hotel
# Register your models here.


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    pass
