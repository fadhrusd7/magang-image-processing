import cv2
import numpy as np

SOURCE = "assets/video_20260905_163428.mp4"  # Ganti 0 untuk webcam bawaan
HSV_LOWER = (90, 90, 80)
HSV_UPPER = (120, 255, 255)
BLUR_SIZE = (11, 11)  # Harus ganjil supaya punya piksel tengah
KERNEL_SIZE = (5, 5)
ITERATIONS = 2
DISPLAY_SCALE = 0.5  # Gabungan dua gambar diperkecil supaya muat di layar
FONT = cv2.FONT_HERSHEY_SIMPLEX
YELLOW = (0, 255, 255)
BLACK = (0, 0, 0)


def make_mask(frame):
    # Piksel di dalam rentang HSV jadi putih (255), sisanya hitam (0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, np.array(HSV_LOWER), np.array(HSV_UPPER))


def clean_mask(frame):
    # Blur meratakan noise, erode membuang bintik, dilate mengembalikan ukuran
    blurred = cv2.GaussianBlur(frame, BLUR_SIZE, 0)
    mask = make_mask(blurred)
    kernel = np.ones(KERNEL_SIZE, np.uint8)
    mask = cv2.erode(mask, kernel, iterations=ITERATIONS)
    return cv2.dilate(mask, kernel, iterations=ITERATIONS)


def add_label(image, text):
    # Tulisan hitam tebal di bawah tulisan kuning supaya terbaca di latar terang
    cv2.putText(image, text, (20, 60), FONT, 2, BLACK, 8)
    cv2.putText(image, text, (20, 60), FONT, 2, YELLOW, 3)


def main():
    cap = cv2.VideoCapture(SOURCE)
    if not cap.isOpened():
        print("Kamera tidak bisa dibuka, cek SOURCE")
        return

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        mask = clean_mask(frame)
        # Mask hanya 1 kanal, diubah jadi 3 kanal supaya bisa ditempel ke frame
        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        add_label(frame, "Sebelum masking")
        add_label(mask_bgr, "Sesudah masking")

        # Kiri frame asli, kanan mask, dalam satu jendela supaya posisinya tetap
        combined = np.hstack((frame, mask_bgr))
        scale = DISPLAY_SCALE
        combined = cv2.resize(combined, None, fx=scale, fy=scale)

        cv2.imshow("Masking", combined)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
