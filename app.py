from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- NEU

import threading, os
import cv2, face_recognition, pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # <--- NEU: CORS aktivieren
LOCK = threading.Lock()

# ------------- Globals -------------
TRAIN_DIR = "train-data"
PKL_PATH  = "trained_faces.pkl"
known_encodings = []
known_names     = []

# ------------- Helper -------------
def load_trained():
    global known_encodings, known_names
    if os.path.exists(PKL_PATH):
        with open(PKL_PATH, "rb") as f:
            known_encodings, known_names = pickle.load(f)

def train_faces():
    encs, names = [], []
    for person in os.listdir(TRAIN_DIR):
        person_path = os.path.join(TRAIN_DIR, person)
        if not os.path.isdir(person_path): continue

        for img_name in os.listdir(person_path):
            img = cv2.imread(os.path.join(person_path, img_name))
            if img is None: continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            e = face_recognition.face_encodings(img, model="cnn")
            if e:
                encs.append(e[0]); names.append(person)
                break  # nur 1 Bild pro Person
    with open(PKL_PATH, "wb") as f:
        pickle.dump((encs, names), f)
    load_trained()

# ------------- Routes -------------
@app.route("/train", methods=["POST"])
def route_train():
    with LOCK:
        train_faces()
    return jsonify({
        "status": "trained",
        "faces": len(known_encodings)
    }), 200

@app.route("/recognize", methods=["POST"])
def route_recognize():
    # Erwartet: multipart/form-data mit field 'image'
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "no image uploaded"}), 400

    # lade Bild aus Bytes
    npimg = cv2.imdecode(
        np.frombuffer(file.read(), np.uint8),
        cv2.IMREAD_COLOR
    )
    rgb = cv2.cvtColor(npimg, cv2.COLOR_BGR2RGB)
    locs = face_recognition.face_locations(rgb)
    encs = face_recognition.face_encodings(rgb, locs)

    results = []
    for enc in encs:
        matches = face_recognition.compare_faces(known_encodings, enc)
        name = "Unbekannt"
        if True in matches:
            name = known_names[matches.index(True)]
        results.append(name)

    return jsonify({"names": results}), 200

# ------------- Main -------------
if __name__ == "__main__":
    load_trained()
    app.run(host="0.0.0.0", port=5000)
