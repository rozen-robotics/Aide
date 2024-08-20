import requests
from users.models import TrainTicket

SERVER_URL = 'http://server_address/api/get_train_data/'


def sync_train_data(train_number):
    response = requests.get(f'{SERVER_URL}{train_number}/')
    if response.status_code == 200:
        data = response.json()

        # Обновление информации о поезде
        global train_number, departure_station, arrival_station, departure_time, arrival_time
        train_number = data['train_number']
        departure_station = data['departure_station']
        arrival_station = data['arrival_station']
        departure_time = data['departure_time']
        arrival_time = data['arrival_time']

        # Очистка текущих данных
        TrainTicket.objects.all().delete()

        # Создание записей о билетах
        for ticket_data in data['tickets']:
            TrainTicket.objects.create(
                user_id=ticket_data['user_id'],
                face_data=ticket_data['face_data'],
                seat_number=ticket_data['seat_number'],
                created_at=ticket_data['created_at']
            )
    else:
        print(f"Ошибка синхронизации данных: {response.status_code}")


# Вызов синхронизации
sync_train_data(2)  # где 2 - это номер поезда
