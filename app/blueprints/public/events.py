import io
import base64
import cv2
import imutils
import numpy
import os

from werkzeug.utils import secure_filename
from flask import current_app, url_for
from flask_socketio import emit
from io import StringIO
from PIL import Image
from app import socketio


@socketio.on("image_stream")
def image_stream(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # Load the cascade
    face_cascade = cv2.CascadeClassifier(
        os.path.join(current_app.root_path, "haarcascade_frontalface_default.xml")
    )

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(numpy.array(pimg), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(numpy.array(pimg), cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    # Draw the rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Process the image frame
    frame = imutils.resize(frame, width=500)
    frame = cv2.flip(frame, 1)
    imgencode = cv2.imencode(".jpg", frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode("utf-8")
    b64_src = "data:image/jpg;base64,"
    stringData = b64_src + stringData
    emit("server_image", stringData)


@socketio.on("connected")
def connected(json):
    current_app.logger.debug("SocketIO Connected : " + str(json))
