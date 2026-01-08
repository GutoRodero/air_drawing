import cv2
from src.hand_tracker import HandTracker
from src.drawing_canvas import DrawingCanvas
from src.utils import is_pinch

cap = cv2.VideoCapture(0)
tracker = HandTracker()

ret, frame = cap.read()
h, w, _ = frame.shape
canvas = DrawingCanvas(w, h)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    landmarks = tracker.find_hand_landmarks(frame)

    if landmarks:
        index_tip = landmarks[8]
        thumb_tip = landmarks[4]

        if is_pinch(index_tip, thumb_tip):
            canvas.draw(index_tip)
            cv2.circle(frame, index_tip, 8, (0, 255, 0), -1)
        else:
            canvas.reset()

    output = canvas.merge_with_frame(frame)

    cv2.putText(output, "Pinça para desenhar | C: limpar | Q: sair",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)

    cv2.imshow("Air Drawing", output)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas.clear()

cap.release()
cv2.destroyAllWindows()
