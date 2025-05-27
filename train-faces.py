import os
import cv2
import face_recognition
import pickle

# Ordner mit Trainingsbildern
TRAIN_DIR = "train-data"
encodings = []
names = []

for person in os.listdir(TRAIN_DIR):
    person_path = os.path.join(TRAIN_DIR, person)

    if not os.path.isdir(person_path):
        continue

    for image_name in os.listdir(person_path):
        image_path = os.path.join(person_path, image_name)
        image = cv2.imread(image_path)

        if image is None:
            print(f"⚠️ Konnte Bild nicht laden: {image_name}")
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Gesichtscodierung mit "cnn"-Modell
        encodings_in_image = face_recognition.face_encodings(image, model="cnn")

        if encodings_in_image:
            encodings.append(encodings_in_image[0])
            names.append(person)
        else:
            print(f"⚠️ Gesicht nicht erkannt: {image_name}")

# Speichert die erlernten Gesichter in einer Datei
with open("trained_faces.pkl", "wb") as f:
    pickle.dump((encodings, names), f)

print("✅ KI-Training abgeschlossen! Gespeicherte Gesichter:", len(encodings))
