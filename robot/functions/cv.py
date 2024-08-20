import cv2
import numpy as np
import io
from PIL import Image

def recognize_face_cords(data):
    """Возвращает координаты"""
    # Read the image from the request
    img = Image.open(io.BytesIO(data))
    img_np = np.array(img)

    # Convert to grayscale
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    # Load a pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Convert faces to a list of dictionaries with standard Python types
    coordinates = [{'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)} for (x, y, w, h) in faces]

    return coordinates