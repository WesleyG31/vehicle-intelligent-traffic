import cv2
import numpy as np

# Cambia esto si quieres otro video
VIDEO_PATH = "../../data/bridge/bridge_cars.mp4"
FRAME_NUMBER = 45  # Cambia a cualquier frame que te guste más

# Leer video
cap = cv2.VideoCapture(VIDEO_PATH)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

if FRAME_NUMBER >= total_frames:
    print(f"⚠️ El video solo tiene {total_frames} frames.")
    FRAME_NUMBER = total_frames - 1

cap.set(cv2.CAP_PROP_POS_FRAMES, FRAME_NUMBER)
ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ No se pudo leer el frame. Intenta con otro número.")
    exit()

# Lista donde guardaremos los puntos seleccionados
points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        print(f"Punto {len(points)}: ({x}, {y})")
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Selecciona 4 puntos", frame)

# Mostrar imagen para marcar puntos
cv2.imshow("Selecciona 4 puntos", frame)
cv2.setMouseCallback("Selecciona 4 puntos", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Resultado final

print(f"\nfps estimados: {fps}")
print("\n✅ Puntos seleccionados:")
for i, pt in enumerate(points):
    print(f"src_pts[{i}] = {pt}")










