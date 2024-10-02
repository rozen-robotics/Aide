from flask import Flask, request, jsonify
from math import cos, sin, radians
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

max_speed = 0.5
last_update_time = 0
left_vel = 0
right_vel = 0
make_coffee_flag = False


def amap(value, from_low, from_high, to_low, to_high):
    normalized_value = (value - from_low) / (from_high - from_low)
    mapped_value = normalized_value * (to_high - to_low) + to_low
    return mapped_value


def polar_to_cartesian(distance, angle_degrees):
    angle_radians = radians(angle_degrees)
    x = distance * cos(angle_radians)
    y = distance * sin(angle_radians)
    return (x, y)


def clamp(value, max_value):
    if value > max_value:
        return max_value
    elif value < -max_value:
        return -max_value
    else:
        return value


@app.route('/joystick', methods=['POST', 'OPTIONS'])
def joystick():
    global left_vel, right_vel, last_update_time

    if request.method == 'OPTIONS':
        return '', 200

    data = request.json
    angle = float(data['angle'])
    distance = amap(float(data['distance']), 0, 200, 0, max_speed)

    x, y = polar_to_cartesian(distance, angle)
    x /= 3

    left_vel = clamp(y + x, max_speed)
    right_vel = clamp(y - x, max_speed)

    if angle > 180:
        left_vel, right_vel = right_vel, left_vel

    if 225 < angle < 315:
        left_vel, right_vel = 0, 0

    left_vel = round(left_vel, 2)
    right_vel = round(right_vel, 2)

    last_update_time = time.time()

    return jsonify({"status": "OK"})


@app.route('/make_coffee', methods=['POST'])
def make_coffee():
    global make_coffee_flag
    make_coffee_flag = True
    return jsonify({"status": "Coffee making initiated"})


@app.route('/get_wheel_values', methods=['GET'])
def get_wheel_values():
    global left_vel, right_vel, last_update_time, make_coffee_flag

    current_time = time.time()
    if current_time - last_update_time > 1:  # Если прошло более 1 секунд с последнего обновления
        left_vel = right_vel = 0

    coffee_status = make_coffee_flag
    make_coffee_flag = False  # Сбрасываем флаг после отправки

    return jsonify({
        "left_vel": left_vel,
        "right_vel": right_vel,
        "make_coffee": coffee_status
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
