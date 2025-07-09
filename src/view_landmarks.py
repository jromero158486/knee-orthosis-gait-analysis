"""
view_landmarks.py  •  Procesa y anota videos con MediaPipe Pose
Más rápido:  •  Reusa un solo PoseDetector  •  Salta N-cuadros  •  Ventana opcional
"""

import cv2, os, sys
from pathlib import Path
from time import time
try:
    from src.pose_utils import PoseDetector
except ModuleNotFoundError:          # ejecución con -m
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from src.pose_utils import PoseDetector

# ---------- Configuración ----------
VIDEO_LIST = [
    (Path("data/videos/sin_ortesis.mp4"), "landmarks_sin_ortesis.mp4"),
    (Path("data/videos/con_ortesis.mp4"), "landmarks_con_ortesis.mp4"),
]
OUT_DIR       = Path("data/outputs/visualizations")
DISPLAY       = True          # False = sin ventana (más rápido)
SAVE_OUTPUT   = True          # False = solo ver
FRAME_STEP    = 2             # procesa 1 de cada 2 cuadros (≈ ×2 velocidad)
# ----------------------------------

OUT_DIR.mkdir(parents=True, exist_ok=True)

# Índices MediaPipe
L_HIP, R_HIP = 23, 24
L_KNEE, R_KNEE = 25, 26
L_ANKLE, R_ANKLE = 27, 28
COL_LEFT, COL_RIGHT, COL_TEXT = (0,255,0), (255,0,0), (0,200,255)

detector = PoseDetector()           # ¡una sola instancia!

def angle(lm, a, b, c):
    return detector.angle(lm, a, b, c)

def draw_leg(frame, lm, hip, knee, ankle, color):
    xh,yh,_ = lm[hip]; xk,yk,_ = lm[knee]; xa,ya,_ = lm[ankle]
    cv2.line(frame,(xh,yh),(xk,yk),color,2)
    cv2.line(frame,(xk,yk),(xa,ya),color,2)
    ang = angle(lm, hip, knee, ankle)
    cv2.putText(frame,f"{int(ang)}°",(xk-20,yk-15),cv2.FONT_HERSHEY_SIMPLEX,0.55,COL_TEXT,2)

def process(video_path: Path, out_name: str):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"[X] No se puede abrir {video_path}"); return

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    w,h = int(cap.get(3)), int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    writer = cv2.VideoWriter(str(OUT_DIR/out_name),fourcc,fps,(w,h)) if SAVE_OUTPUT else None

    if DISPLAY:
        cv2.namedWindow(out_name, cv2.WINDOW_NORMAL); cv2.resizeWindow(out_name, 800,450)

    frame_id, t0 = 0, time()
    while True:
        ret, frame = cap.read()
        if not ret: break
        if frame_id % FRAME_STEP:        # saltar cuadros
            frame_id += 1
            continue

        lm = detector.get_landmarks(frame)
        if lm:
            for idx in (L_HIP,L_KNEE,L_ANKLE,R_HIP,R_KNEE,R_ANKLE):
                x,y,_ = lm[idx]; cv2.circle(frame,(x,y),5,(0,255,255),-1)
            draw_leg(frame,lm,L_HIP,L_KNEE,L_ANKLE,COL_LEFT)
            draw_leg(frame,lm,R_HIP,R_KNEE,R_ANKLE,COL_RIGHT)

        if DISPLAY:
            cv2.imshow(out_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
        if writer: writer.write(frame)
        frame_id += 1

    # --- Limpieza ---
    cap.release(); writer.release() if writer else None
    if DISPLAY: cv2.destroyWindow(out_name)
    print(f"[✓] {out_name} listo – procesado en {time()-t0:.1f} s")

def main():
    for vid,out in VIDEO_LIST:
        if vid.exists(): process(vid,out)
        else: print(f"[!] {vid} no encontrado – saltado.")

if __name__ == "__main__":
    main()