import io
import base64

from flask import current_app
from flask_socketio import emit
from io import StringIO
from PIL import Image
from app import socketio


@socketio.on("image_stream")
def image_stream(data_image):
    current_app.logger.debug("Receive Image...")
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # Process the image frame
    frame = imutils.resize(frame, width=700)
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
