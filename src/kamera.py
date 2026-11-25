import cv2

SOURCE = "assets/video_20260905_163428.mp4"  # Ganti 0 untuk webcam bawaan


def main():
    cap = cv2.VideoCapture(SOURCE)
    if not cap.isOpened():
        print("Kamera tidak bisa dibuka, cek SOURCE")
        return

    printed = False
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # Frame adalah array numpy berukuran (tinggi, lebar, kanal)
        if not printed:
            height, width, channels = frame.shape
            print(f"Ukuran frame: tinggi={height}, lebar={width}, kanal={channels}")
            print("Titik (0, 0) di kiri atas, x ke kanan, y ke bawah")
            printed = True

        cv2.imshow("Kamera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
