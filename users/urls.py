from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views
from users.views import *
from users.syncdb import *

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
]
