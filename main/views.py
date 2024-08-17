
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from users.models import TrainTicket, BiometricProfile
from services.biometrics import register_face, recognize_face

def index(request):
    return (render(request, 'main/index.html'))



@login_required
def check_in(request):
    if request.method == 'POST':
        train_ticket_id = request.POST.get('train_ticket_id')
        photo_data = request.POST.get('photo_data')

        # Найти билет
        try:
            train_ticket = TrainTicket.objects.get(id=train_ticket_id, user=request.user)
        except TrainTicket.DoesNotExist:
            return HttpResponse("Билет не найден", status=404)

        if not BiometricProfile.objects.filter(user=request.user).exists():
            if photo_data:
                # Регистрация лица в биометрической базе
                if not register_face(photo_data, request.user):
                    return render(request, 'main/check_in.html',
                                  context={'error': "Ваше лицо не видно, попробуйте еще раз!"})
            else:
                return render(request, 'main/check_in.html', context={'error': "Вы не отсканировали лицо!"})

        return redirect('index')  # перенаправление на страницу успешной регистрации

    return render(request, 'main/check_in.html',
                  context={'is_bio': BiometricProfile.objects.filter(user=request.user).exists()})
