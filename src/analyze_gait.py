import cv2
import pandas as pd
from src.pose_utils import PoseDetector
import os

# Ruta de entrada de videos y salida de resultados
VIDEO_DIR = r"C:\Users\User\Desktop\gait_analysis_orthosis\data\videos"
OUTPUT_CSV = r"C:\Users\User\Desktop\gait_analysis_orthosis\data\outputs\metrics_csv\gait_metrics.csv"

# Lista de videos con etiquetas de condición
videos = [
    ("con_ortesis.mp4", "con_ortesis"),
    ("sin_ortesis.mp4", "sin_ortesis")
]

# Detector de pose
detector = PoseDetector()
all_data = []

# Procesar cada video
for filename, condicion in videos:
    path = os.path.join(VIDEO_DIR, filename)
    cap = cv2.VideoCapture(path)
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        lm = detector.get_landmarks(frame)
        if lm:
            row = {
                "condicion": condicion,
                "frame": frame_id
            }
            # Ángulo de rodilla derecha (cadera, rodilla, tobillo)
            row["knee_angle_R"] = detector.angle(lm, 24, 26, 28)
            # Ángulo de rodilla izquierda (cadera, rodilla, tobillo)
            row["knee_angle_L"] = detector.angle(lm, 23, 25, 27)
            # Desviación de la línea media
            row["midline_dev"] = detector.midline_deviation(lm)
            all_data.append(row)

        frame_id += 1

    cap.release()

# Guardar resultados en CSV
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df = pd.DataFrame(all_data)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Resultados guardados en {OUTPUT_CSV}")