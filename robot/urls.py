from django.contrib import admin
from django.urls import path, include
from robot import views

urlpatterns = [
    path('departure/', views.departure_index, name='departure_index'),
    path('recognize_face_ajax/', views.recognize_face_ajax, name='recognize_face_ajax'),

    path('routine/', views.routine, name='routine'),
    path('process_question_ajax/', views.process_question_ajax, name='process_question_ajax'),
    path('recognize_face_cords_ajax/', views.recognize_face_cords_ajax, name='recognize_face_cords_ajax'),

    path('process_audio_ajax/', views.process_audio_ajax, name='process_audio_ajax'),

]
