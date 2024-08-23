import json

from django.http import JsonResponse
from django.shortcuts import render
from conditions import send_to_robot
from conditions.send_to_robot import process_order
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def change_condition(request):
    if request.method == 'POST':
        try:
            # Парсинг JSON данных из тела запроса
            data = json.loads(request.body.decode('utf-8'))
            condition = data.get('condition')
            if condition == "process_order":
                order_id = data.get('order_id')
                seat_id = data.get('seat_id')
                # Вызов функции для обработки заказа
                process_order(order_id, seat_id)
                return JsonResponse({'status': 'success'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid condition'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
