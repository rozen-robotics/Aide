import base64

from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from users.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class MyLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm


from .models import TrainCruise, TrainTicket


def get_train_data(request, train_number):
    try:
        train = TrainCruise.objects.get(train_number=train_number)
        tickets = TrainTicket.objects.filter(train=train)
        response_data = {
            'train_number': train.train_number,
            'departure_station': train.departure_station,
            'arrival_station': train.arrival_station,
            'departure_time': train.departure_time,
            'arrival_time': train.arrival_time,
            'tickets': [
                {
                    'user_id': ticket.user.id,
                    'face_data': base64.b64encode(ticket.user.biometricprofile.face_data).decode('utf-8') if ticket.user.biometricprofile else None,
                    'seat_number': ticket.seat_number,
                    'created_at': ticket.created_at,
                    'user_name': f"{ticket.user.first_name} {ticket.user.last_name}",
                } for ticket in tickets
            ]
        }
        return JsonResponse(response_data, status=200)
    except TrainCruise.DoesNotExist:
        return JsonResponse({'error': 'Train not found'}, status=404)