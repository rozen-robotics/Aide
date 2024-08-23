from django.contrib import admin
from django.urls import path, include
from conditions import views

urlpatterns = [
    path('change_condition', views.change_condition, name='change_condition'),

]
