import cv2

SOURCE = "assets/video_20260905_163428.mp4"  # Ganti 0 untuk webcam bawaan
LINE_POSITION = 0.5  # Garis batas di 50% tinggi frame (tengah)
FONT = cv2.FONT_HERSHEY_SIMPLEX
RED = (0, 0, 255)


def get_area_below_line(frame):
    # Slicing frame[y:, :] artinya baris y sampai bawah, semua kolom
    height = frame.shape[0]
    line_y = int(height * LINE_POSITION)
    return frame[line_y:, :].copy(), line_y


def draw_line(frame, line_y):
    width = frame.shape[1]
    cv2.line(frame, (0, line_y), (width, line_y), RED, 3)
    cv2.putText(frame, "Batas", (20, line_y - 15), FONT, 1, RED, 2)


def main():
    cap = cv2.VideoCapture(SOURCE)
    if not cap.isOpened():
        print("Kamera tidak bisa dibuka, cek SOURCE")
        return

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # Area diambil sebelum frame digambari supaya isinya tetap bersih
        area_below, line_y = get_area_below_line(frame)
        draw_line(frame, line_y)

        cv2.imshow("Garis batas", frame)
        cv2.imshow("Area di bawah garis", area_below)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
