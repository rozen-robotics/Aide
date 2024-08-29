from django.contrib import admin
from django.urls import path, include
from conditions import views

urlpatterns = [
    path('process_order_ajax', views.process_order_ajax, name='process_order_ajax'),

    path('start_talking_ajax/', views.start_talking_ajax, name='start_talking_ajax'),
    path('stop_talking_ajax/', views.stop_talking_ajax, name='stop_talking_ajax'),
]
