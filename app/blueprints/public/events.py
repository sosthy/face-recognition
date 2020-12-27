import io
import base64
import cv2
import imutils
import numpy
import os
import pickle

from werkzeug.utils import secure_filename
from flask import current_app, url_for
from flask_socketio import emit
from io import StringIO
from PIL import Image
from app import socketio

# Load the cascade
face_cascade = cv2.CascadeClassifier(
    os.path.join("app/haarcascade_frontalface_default.xml")
)

labels = {}
labels_path = os.path.join("app/labels.pickle")
with open(labels_path, "rb") as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

recognizer = cv2.face.LBPHFaceRecognizer_create()
trainner_path = os.path.join("app/trainner.yml")
recognizer.read(trainner_path)


@socketio.on("image_stream")
def image_stream(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(numpy.array(pimg), cv2.COLOR_RGB2BGR)
    # Process the image frame
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.05, minNeighbors=5, minSize=(25, 25)
    )

    # Draw the rectangle around the faces
    for (x, y, w, h) in faces:

        roi_gray = gray[y : y + h, x : x + w]
        roi_color = frame[y : y + h, x : x + w]

        # recognize
        id_, conf = recognizer.predict(roi_gray)

        if conf <= 85:
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 1
            cv2.putText(frame, name, (x, y - 5), font, 0.5, color, stroke, cv2.LINE_AA)

        end_cord_x = x + w
        end_cord_y = y + h
        color = (0, 255, 0)
        stroke = 2
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

    imgencode = cv2.imencode(".jpg", frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode("utf-8")
    b64_src = "data:image/jpg;base64,"
    stringData = b64_src + stringData
    emit("server_image", stringData)


@socketio.on("connected")
def connected(json):
    current_app.logger.debug("SocketIO Connected : " + str(json))
