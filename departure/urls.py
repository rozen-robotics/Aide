from django.contrib import admin
from django.urls import path, include
from departure import views

urlpatterns = [
    path('', views.departure_index, name='departure_index'),
    path('recognize_face_ajax/', views.recognize_face_ajax, name='recognize_face_ajax'),
]
