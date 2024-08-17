from django.contrib import admin
from django.urls import path, include
from robot import views

urlpatterns = [
    path('departure/', views.departure_index, name='departure_index'),
    path('recognize_face_ajax/', views.recognize_face_ajax, name='recognize_face_ajax'),
]
