import numpy as np
import cv2

class DrawingCanvas:
    def __init__(self, width, height):
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.prev_point = None
        self.color = (255, 0, 255)
        self.thickness = 6

    def draw(self, point):
        if self.prev_point is None:
            self.prev_point = point
            return

        cv2.line(self.canvas, self.prev_point, point, self.color, self.thickness)
        self.prev_point = point

    def reset(self):
        self.prev_point = None

    def clear(self):
        self.canvas = np.zeros_like(self.canvas)

    def merge_with_frame(self, frame):
        return cv2.add(frame, self.canvas)
