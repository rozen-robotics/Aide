import json

from django.http import JsonResponse
from django.shortcuts import render
from conditions import send_to_robot
from conditions.send_to_robot import process_order, start_talking, stop_talking
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process_order_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            process_order(data)
            return JsonResponse({'status': 'success'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def start_talking_ajax(request):
    try:
        start_talking()
        return JsonResponse({'status': 'success'}, status=200)
    except:
        return JsonResponse({'error': 'Error'}, status=400)

@csrf_exempt
def stop_talking_ajax(request):
    try:
        stop_talking()
        return JsonResponse({'status': 'success'}, status=200)
    except:
        return JsonResponse({'error': 'Error'}, status=400)