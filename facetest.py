import cv2
import face_recognition
import pickle
import threading

# Gelernte Gesichter laden
with open("trained_faces.pkl", "rb") as f:
    known_encodings, known_names = pickle.load(f)

# Kamera mit DirectShow für bessere Performance öffnen
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
video_capture.set(cv2.CAP_PROP_FPS, 30)  # Versucht 30 FPS zu setzen
video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))  # Bessere Performance mit MJPG
video_capture.set(3, 640)  # Breite
video_capture.set(4, 480)  # Höhe

frame = None
face_locations = []
face_encodings = []
face_names = []
lock = threading.Lock()
  

def process_frame():
    global frame, face_locations, face_encodings, face_names
    while True:
        with lock:
            if frame is None:
                continue
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        detected_locations = face_recognition.face_locations(rgb_small_frame)
        detected_encodings = face_recognition.face_encodings(rgb_small_frame, detected_locations)

        detected_names = []
        for encoding in detected_encodings:
            matches = face_recognition.compare_faces(known_encodings, encoding)
            name = "Unbekannt"
            if True in matches:
                name = known_names[matches.index(True)]
            detected_names.append(name)

        with lock:
            face_locations = [(top * 2, right * 2, bottom * 2, left * 2) for (top, right, bottom, left) in detected_locations]
            face_encodings = detected_encodings
            face_names = detected_names


# Startet die Gesichtserkennung in einem separaten Thread
thread = threading.Thread(target=process_frame, daemon=True)
thread.start()

while True:
    ret, new_frame = video_capture.read()
    if not ret:
        break

    with lock:
        frame = new_frame.copy()

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
