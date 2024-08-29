import json
import urllib.request
import urllib.parse
from django.conf import settings


def procces_order(order, seat):
    ai_url = f'http://{settings.ROBOT_SERVER_URL}/conditions/process_order_ajax'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(
        {'condition': 'process_order', 'order_id': order.id, 'product_id': order.product.id,
         'product_name': order.product.name, 'product_category': order.product.category, 'seat_id': seat}).encode(
        'utf-8')

    req = urllib.request.Request(ai_url, data=payload, headers=headers)
    with urllib.request.urlopen(req) as response:
        response_data = json.loads(response.read().decode('utf-8'))
