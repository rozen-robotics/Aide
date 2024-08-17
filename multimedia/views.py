from yoomoney import Quickpay, Client
from django.conf import settings
from django.shortcuts import render, redirect
from multimedia.models import UserOrder, Product
from django.contrib.auth.decorators import login_required
import uuid
from RobotStuartRzd.keys import youmoney_token
from robot_functions.functions import procces_order
from users.models import User, TrainTicket

@login_required
def create_payment(request, product):
    user = request.user
    label = str(uuid.uuid4())  # Генерация уникальной метки

    sum = Product.objects.get(id=product).price

    quickpay = Quickpay(
        receiver="4100118786548312",
        quickpay_form="shop",
        targets="Покупка на Портале ВСМ",
        paymentType="AC",  # Тип оплаты (AC — с карты, PC — из кошелька)
        sum=sum,  # Цена товара
        label=label,
        successURL=request.build_absolute_uri('/multimedia/check-payment-status/')
    )

    # Сохранение подписки с пометкой
    order = UserOrder.objects.create(
        user=user,
        yoomoney_label=label,
        product=Product.objects.get(id=product),

    )

    return redirect(quickpay.redirected_url)

@login_required
def check_payment_status(request):
    user = request.user
    order = UserOrder.objects.filter(user=user, is_active=False).last()
    token = youmoney_token  # Замените на ваш токен
    client = Client(token)
    try:
        # Проверка операции с использованием метки
        history = client.operation_history(label=order.yoomoney_label)
        if history.operations:
            operation = history.operations[0]
            if operation.status == 'success':
                # Если оплата успешна, активируйте подписку
                order.is_active = True
                order.save()
                procces_order(order.id, TrainTicket.objects.filter(user=user).last().seat_number) #запрос к роботу
                return render(request, 'multimedia/success.html')
    except:
        pass

    return render(request, 'multimedia/failure.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'multimedia/product_list.html', {'products': products})

def multimedia_index(request):
    best_product = Product.objects.first()
    return render(request, 'multimedia/multimedia_index.html', {'best_product': best_product})

def films(request):
    return render(request, 'multimedia/films.html')

def music(request):
    return render(request, 'multimedia/music.html')
