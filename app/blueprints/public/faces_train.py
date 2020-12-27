import os, numpy, cv2, pickle
from PIL import Image
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.models import User

engine = create_engine("sqlite:///app/db.sqlite")

IMAGE_DIR = os.path.join(os.path.abspath("app/static/uploads"))

# Load the cascade
face_cascade = cv2.CascadeClassifier("app/haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
labels_ids = {}
y_labels = []
x_train = []
i = 0

for root, dirs, files in os.walk(IMAGE_DIR):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            # Get label
            filename = os.path.basename(path)

            # list of first element of each row (i.e. User objects)
            stmt = engine.execute(
                "SELECT id, login, photo FROM user WHERE photo='" + filename + "'"
            )

            user = stmt.fetchone()

            if user:
                label = user[1]
                labels_ids[label] = user[0]
                id_ = user[0]
                pil_image = Image.open(os.path.join(root, user[2])).convert("L")
                image_array = numpy.array(pil_image, "uint8")

                faces = face_cascade.detectMultiScale(
                    image_array, scaleFactor=1.05, minNeighbors=4, minSize=(20, 20)
                )

                # Draw the rectangle around the faces
                for (x, y, w, h) in faces:
                    roi = image_array[y : y + h, x : x + w]
                    x_train.append(roi)
                    y_labels.append(id_)

with open("app/labels.pickle", "wb") as f:
    pickle.dump(labels_ids, f)

if x_train.__len__() > 0:
    recognizer.train(x_train, numpy.array(y_labels))
    recognizer.save("app/trainner.yml")
