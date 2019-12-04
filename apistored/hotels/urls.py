from django.urls import path

from . import views

urlpatterns = [
    path('hotels/', views.HotelList.as_view(), name='hotel_list'),
]
