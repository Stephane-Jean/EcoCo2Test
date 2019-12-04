from django.urls import path

from . import views

urlpatterns = [
    path('', views.retrieve, name='retrieve'),
    path('csv_url/', views.csvGeneration, name='csvGeneration'),
]
