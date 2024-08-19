from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from users.models import TrainTicket, BiometricProfile, RobotProfile
from services.biometrics import register_face, recognize_face

@login_required(login_url='login')
def departure_index(request):
    try:
        cruise = RobotProfile.objects.get(user=request.user).now_cruise
    except:
        return JsonResponse({'status': 'error', 'message': 'You are not a Stewart Robot or dont you have a current train.'})
    return (render(request, 'robot/departure.html', context={'cruise': cruise}))

@login_required(login_url='login')
def recognize_face_ajax(request):
    if request.method == 'POST':
        photo_data = request.POST.get('photo_data')
        cruise_id = RobotProfile.objects.get(user=request.user).now_cruise

        if photo_data:
            recognize_result = recognize_face(photo_data, cruise_id)
            if recognize_result == 0:
                return JsonResponse({'status': 'no_face'})
            elif recognize_result == 1:
                return JsonResponse({'status': 'not_registered'})
            else:
                return JsonResponse({'status': 'success', 'data': recognize_result})

    return JsonResponse({'status': 'error', 'message': 'Некорректный запрос.'})


@login_required(login_url='login')
def voice_controll_test(request):
    try:
        cruise = RobotProfile.objects.get(user=request.user).now_cruise
    except:
        return JsonResponse({'status': 'error', 'message': 'You are not a Stewart Robot or dont you have a current train.'})
    return (render(request, 'robot/voice_controll_test.html', context={'cruise': cruise}))
