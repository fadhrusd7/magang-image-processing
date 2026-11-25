import cv2
import numpy as np

SOURCE = "assets/video_20260905_163428.mp4"  # Ganti 0 untuk webcam bawaan
MASK_WINDOW = "Mask"
INITIAL_VALUES = {
    "H min": 90,
    "S min": 90,
    "V min": 80,
    "H max": 120,
    "S max": 255,
    "V max": 255,
}
MAX_VALUES = {"H": 179, "S": 255, "V": 255}  # Hue di OpenCV hanya 0 sampai 179
FONT = cv2.FONT_HERSHEY_SIMPLEX
GREEN = (0, 255, 0)


def ignore(_):
    # createTrackbar wajib diberi fungsi, tapi nilainya kita baca sendiri
    pass


def create_trackbars():
    cv2.namedWindow(MASK_WINDOW)
    for name, value in INITIAL_VALUES.items():
        cv2.createTrackbar(name, MASK_WINDOW, value, MAX_VALUES[name[0]], ignore)


def read_trackbars():
    # Kembalikan (lower, upper), masing-masing berisi (H, S, V)
    values = [cv2.getTrackbarPos(name, MASK_WINDOW) for name in INITIAL_VALUES]
    return tuple(values[:3]), tuple(values[3:])


def draw_values(frame, lower, upper):
    cv2.putText(frame, f"Bawah: {lower}", (10, 40), FONT, 1, GREEN, 2)
    cv2.putText(frame, f"Atas: {upper}", (10, 80), FONT, 1, GREEN, 2)


def main():
    cap = cv2.VideoCapture(SOURCE)
    if not cap.isOpened():
        print("Kamera tidak bisa dibuka, cek SOURCE")
        return

    create_trackbars()
    lower, upper = read_trackbars()
    while True:
        ok, frame = cap.read()
        if not ok:
            # Video habis, putar ulang dari awal supaya bisa terus menyetel
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower, upper = read_trackbars()
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        ball_only = cv2.bitwise_and(frame, frame, mask=mask)

        draw_values(frame, lower, upper)
        cv2.imshow("Kamera", frame)
        cv2.imshow(MASK_WINDOW, mask)
        cv2.imshow("Hanya warna bola", ball_only)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    print(f"Salin ke file lain: HSV_LOWER = {lower}, HSV_UPPER = {upper}")
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
