from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

from users.models import TrainTicket


admin.site.register(TrainTicket)

