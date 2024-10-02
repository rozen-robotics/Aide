from flask import Flask, request, render_template
import odrive
import time
from math import cos, sin, radians
import subprocess

max_speed = 0.5
app = Flask(__name__)

#log.info('Connecting...')
# odrv0 = odrive.find_any()
#log.success('Connected!')

is_coffe_making = False

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/move', methods=['POST'])
def move():
    if is_coffe_making:
        return 'OK'
    angle = float(request.form['angle'])
    distance = amap(float(request.form['distance']), 0, 200, 0, max_speed)
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

    print(f'{left_vel}     {right_vel}\n')

    # odrv0.axis0.controller.input_vel = left_vel
    # odrv0.axis1.controller.input_vel = right_vel

    return 'OK'


@app.route('/make_coffee', methods=['POST'])
def make_coffee():
    global is_coffe_making
    is_coffe_making = True
    from coffe import make_coffe
    make_coffe()
    is_coffe_making = False
    return 'Coffee making initiated'


@app.route('/say_phrase', methods=['POST'])
def say_phrase():
    phrase_number = request.form['value']
    audio_file = f"{phrase_number}.wav"
    subprocess.run(["aplay", audio_file])
    return f'Playing phrase {phrase_number}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
