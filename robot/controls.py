import requests
import time
import odrive
from coffe import make_coffe

SERVER_URL = "http://90.156.203.227:8000"

# odrv0 = odrive.find_any()

def get_wheel_values():
    try:
        response = requests.get(f"{SERVER_URL}/get_wheel_values")
        if response.status_code == 200:
            data = response.json()
            return data["left_vel"], data["right_vel"], data["make_coffee"]
        else:
            print(f"Ошибка при получении данных: {response.status_code}")
            return 0, 0, False
    except Exception as e:
        print(f"Ошибка при подключении к серверу: {e}")
        return 0, 0, False


def make_coffee():
    print("Робот начал приготовление кофе!")
    make_coffe()
    print("Кофе готов!")


def main():
    while True:
        left_vel, right_vel, coffee_flag = get_wheel_values()
        print(f"Левое колесо: {left_vel}, Правое колесо: {right_vel}")

        if coffee_flag:
            make_coffee()

        # set_motor_speed(left_motor, left_vel)
        # set_motor_speed(right_motor, right_vel)

        time.sleep(0.5)  # Пауза 0.5 секунды перед следующим запросом


if __name__ == "__main__":
    main()
