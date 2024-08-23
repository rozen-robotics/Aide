from django.contrib import admin
from django.urls import path, include
from robot import views

urlpatterns = [
    path('departure/', views.departure_index, name='departure_index'),
    path('recognize_face_ajax/', views.recognize_face_ajax, name='recognize_face_ajax'),

    path('voice_controll_test/', views.voice_controll_test, name='voice_controll_test'),
    path('process_question_ajax/', views.process_question_ajax, name='process_question_ajax'),
    path('recognize_face_cords_ajax/', views.recognize_face_cords_ajax, name='recognize_face_cords_ajax')
]
