# 🧠 IDentifAI – Gesichtserkennung für Schulklassen

Ein Schulprojekt zur automatischen Gesichtserkennung mit KI (Python + Flask + face_recognition). Ideal für Stundenpläne, Anwesenheit oder Infoanzeigen im Klassenzimmer.

## 📦 Features

- Gesichtstrainierung durch Upload von Fotos
- Wiedererkennung über Kamera oder Foto
- Speicherbare Gesichter pro Klasse
- Webinterface (HTML + JS)
- Backend mit Flask & OpenCV

## 🚀 Installation

### 🔧 Voraussetzungen

- Python 3.x
- Git
- pip

### 🔥 Setup lokal

```bash
git clone https://github.com/BiH-PlayerA/IDentifAI.git
cd IDentifAI
pip install -r requirements.txt
python app.py
```

### 📁 Ordnerstruktur für Trainingsdaten

train-data/
├── Max Mustermann/
│ └── bild1.jpg
├── Maxi Mustmann/
│ └── bild1.png
