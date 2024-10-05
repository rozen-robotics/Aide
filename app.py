import pyaudio
from flask import Flask, request, render_template
import odrive
import time
from math import cos, sin, radians
import subprocess
import random

max_speed = 0.5
app = Flask(__name__)

# log.info('Connecting...')
# odrv0 = odrive.find_any()
# log.success('Connected!')

is_coffe_making = False
is_speaking = False


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


def speak_audio_by_disk(path):
    global is_speaking
    if is_speaking or is_coffe_making:
        return
    
    is_speaking = True
    player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    with open(path, 'rb') as wav_file:
        wav_data = wav_file.read()

    chunk_size = 1024
    for i in range(0, len(wav_data), chunk_size):
        chunk = wav_data[i:i + chunk_size]
        player_stream.write(chunk)

    player_stream.stop_stream()
    player_stream.close()
    is_speaking = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/move', methods=['POST'])
def move():
    if is_coffe_making or is_speaking:
        return 'Робот занят'
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
    if is_coffe_making or is_speaking:
        return 'Робот занят'
    is_coffe_making = True
    from coffe import make_coffe
    speak_audio_by_disk('audio/make_coffe.wav')
    make_coffe()
    speak_audio_by_disk('audio/coffe_done.wav')
    is_coffe_making = False
    return 'Кофе приготовлен'


@app.route('/say_phrase', methods=['POST'])
def say_phrase():
    if is_coffe_making or is_speaking:
        return 'Робот занят'
    phrase_number = request.form['value']
  
    audio_file = f"audio/{phrase_number}/{random.randint(0, 4)}.wav"

    speak_audio_by_disk(audio_file)

    print(f"Воспроизведение {audio_file}")
    return f'Фраза {phrase_number} воспроизведена'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
