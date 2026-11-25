import cv2
import numpy as np

SOURCE = "assets/video_20260905_163428.mp4"  # Ganti 0 untuk webcam bawaan
HSV_LOWER = (90, 90, 80)
HSV_UPPER = (120, 255, 255)
MIN_RADIUS = 10
LINE_POSITION = 0.5  # Garis batas di 50% tinggi frame (tengah)
FONT = cv2.FONT_HERSHEY_SIMPLEX
RED = (0, 0, 255)


def find_ball(frame):
    # Versi singkat dari kontur.py, kembalikan (x, y, radius) atau None
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(HSV_LOWER), np.array(HSV_UPPER))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    (x, y), radius = cv2.minEnclosingCircle(max(contours, key=cv2.contourArea))
    if radius < MIN_RADIUS:
        return None
    return int(x), int(y), int(radius)


def decide_action(ball, line_y):
    # Stop kalau titik tengah bola sudah melewati garis batas
    if ball is None:
        return "Lurus"
    center_y = ball[1]
    return "Stop" if center_y > line_y else "Lurus"


def main():
    cap = cv2.VideoCapture(SOURCE)
    if not cap.isOpened():
        print("Kamera tidak bisa dibuka, cek SOURCE")
        return

    last_action = None
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        height, width = frame.shape[:2]
        line_y = int(height * LINE_POSITION)
        action = decide_action(find_ball(frame), line_y)
        if action != last_action:
            print(f"Aksi: {action}")
            last_action = action

        cv2.line(frame, (0, line_y), (width, line_y), RED, 3)
        cv2.putText(frame, f"Aksi: {action}", (20, 60), FONT, 1.5, RED, 3)
        cv2.imshow("Keputusan", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
