from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    AuthenticationForm as DjangoAuthenticationForm)
from django.contrib.auth import get_user_model, authenticate
from django import forms
from django.utils. translation import gettext_lazy as _
from django.core.exceptions import ValidationError

User = get_user_model()


class AuthenticationForm(DjangoAuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )

        return self.cleaned_data


class UserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(label=_("Email"),
        max_length=254,
        widget = forms.EmailInput(attrs={'autocomplete': 'email'})
                             )
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ("username", "email")

