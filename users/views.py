from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from users.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class MyLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm

