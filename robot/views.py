import base64
import json
import urllib.request
import urllib.parse

from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from users.models import TrainTicket, TrainInfo
from services.biometrics import recognize_face
from users.syncdb import sync_train_data
from robot.functions.cv import recognize_face_cords
from robot.functions.speech_recognition import recognize_speech_from_audio  # Импорт функции распознавания речи

def departure_index(request):
    sync_train_data()
    return render(request, 'robot/departure.html')

def recognize_face_ajax(request):
    if request.method == 'POST':
        photo_data = request.POST.get('photo_data')
        cruise_id = TrainInfo.train_number

        if photo_data:
            recognize_result = recognize_face(photo_data, cruise_id)
            if recognize_result == 0:
                return JsonResponse({'status': 'no_face'})
            elif recognize_result == 1:
                return JsonResponse({'status': 'not_registered'})
            else:
                return JsonResponse({'status': 'success', 'data': recognize_result})
    return JsonResponse({'status': 'error', 'message': 'Некорректный запрос.'})

def routine(request):
    return render(request, 'robot/routine.html')

def recognize_face_cords_ajax(request):
    if request.method == 'POST':
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Content-Type must be application/json'}, status=400)

        data = json.loads(request.body.decode('utf-8'))
        photo_data = data.get('photo_data')

        if not photo_data:
            return JsonResponse({'error': 'No photo data provided'}, status=400)

        image_data = base64.b64decode(photo_data)
        coordinates = recognize_face_cords(image_data)
        return JsonResponse(coordinates, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def process_question_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('text', '')

            ai_url = 'https://foteapi2.pythonanywhere.com/process'
            headers = {'Content-Type': 'application/json'}
            payload = json.dumps({'request_type': 'robot_question_answering', 'text': question}).encode('utf-8')

            req = urllib.request.Request(ai_url, data=payload, headers=headers)
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))

            return JsonResponse({'response': response_data})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Произошла ошибка при генерации ответа'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def process_audio_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            audio_data = data.get('audio_data', '')

            if not audio_data:
                return JsonResponse({'error': 'No audio data provided'}, status=400)

            audio_bytes = base64.b64decode(audio_data)
            transcript = recognize_speech_from_audio(audio_bytes)

            return JsonResponse({'transcript': transcript})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Произошла ошибка при обработке аудио'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)