import cv2
import time
from src.hand_tracker import HandTracker
from src.drawing_canvas import DrawingCanvas
from src.utils import finger_touching_thumb

cap = cv2.VideoCapture(0)
tracker = HandTracker()

ret, frame = cap.read()
h, w, _ = frame.shape
canvas = DrawingCanvas(w, h, cube_size=20)

gesture_start_time = None
active_mode = None  # "draw" | "erase"

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    landmarks = tracker.find_hand_landmarks(frame)

    if landmarks:
        thumb = landmarks[4]
        index_finger = landmarks[8]
        middle_finger = landmarks[12]

        if finger_touching_thumb(thumb, index_finger):
            if active_mode != "draw":
                gesture_start_time = time.time()
                active_mode = "draw"

            if time.time() - gesture_start_time >= 1.0:
                canvas.draw_cube(index_finger)
                cv2.circle(frame, index_finger, 6, (0, 255, 0), -1)

        elif finger_touching_thumb(thumb, middle_finger):
            if active_mode != "erase":
                gesture_start_time = time.time()
                active_mode = "erase"

            if time.time() - gesture_start_time >= 1.0:
                canvas.erase_cube(middle_finger)
                cv2.circle(frame, middle_finger, 6, (0, 0, 255), -1)

        else:
            gesture_start_time = None
            active_mode = None

    output = canvas.merge_with_frame(frame)

    cv2.putText(
        output,
        "Indicador = desenhar | Medio = borracha | C: limpar | Q: sair",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow("Voxel Air Drawing", output)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas.clear()

cap.release()
cv2.destroyAllWindows()
