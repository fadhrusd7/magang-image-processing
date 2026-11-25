import cv2
import numpy as np

SOURCE = "assets/video_20260905_163428.mp4"  # Ganti 0 untuk webcam bawaan
HSV_LOWER = (90, 90, 80)
HSV_UPPER = (120, 255, 255)
BLUR_SIZE = (11, 11)
KERNEL_SIZE = (5, 5)
ITERATIONS = 2
MIN_RADIUS = 10  # Lingkaran lebih kecil dari ini dianggap noise
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)
RED = (0, 0, 255)


def make_mask(frame):
    # Langkah dari mask.py: blur, ambil warna, erode, dilate
    blurred = cv2.GaussianBlur(frame, BLUR_SIZE, 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(HSV_LOWER), np.array(HSV_UPPER))
    kernel = np.ones(KERNEL_SIZE, np.uint8)
    mask = cv2.erode(mask, kernel, iterations=ITERATIONS)
    return cv2.dilate(mask, kernel, iterations=ITERATIONS)


def find_ball(contours):
    # Kembalikan (x, y, radius) bola terbesar, atau None kalau tidak ada
    if not contours:
        return None

    largest = max(contours, key=cv2.contourArea)
    (x, y), radius = cv2.minEnclosingCircle(largest)
    if radius < MIN_RADIUS:
        return None
    return int(x), int(y), int(radius)


def main():
    cap = cv2.VideoCapture(SOURCE)
    if not cap.isOpened():
        print("Kamera tidak bisa dibuka, cek SOURCE")
        return

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        mask = make_mask(frame)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, GREEN, 2)

        ball = find_ball(contours)
        if ball is not None:
            x, y, radius = ball
            cv2.circle(frame, (x, y), radius, YELLOW, 3)
            cv2.circle(frame, (x, y), 5, RED, -1)
            print(f"Pusat bola: x={x}, y={y}, radius={radius}")

        cv2.imshow("Kontur", frame)
        cv2.imshow("Mask", mask)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
