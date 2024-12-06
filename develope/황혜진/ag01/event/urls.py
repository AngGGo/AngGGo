from django.urls import path, include
from . import views

app_name = 'event'
urlpatterns = [
    path('calendar/', views.calendar, name='calendar'),
    path('apply/', views.apply, name='apply'),
]

