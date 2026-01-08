import numpy as np
import cv2

class DrawingCanvas:
    def __init__(self, width, height, cube_size=20):
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.cube_size = cube_size
        self.draw_color = (0, 255, 255)

    def _get_cube_coords(self, point):
        x, y = point
        grid_x = (x // self.cube_size) * self.cube_size
        grid_y = (y // self.cube_size) * self.cube_size
        return grid_x, grid_y

    def draw_cube(self, point):
        gx, gy = self._get_cube_coords(point)
        cv2.rectangle(
            self.canvas,
            (gx, gy),
            (gx + self.cube_size, gy + self.cube_size),
            self.draw_color,
            -1
        )

    def erase_cube(self, point):
        gx, gy = self._get_cube_coords(point)
        cv2.rectangle(
            self.canvas,
            (gx, gy),
            (gx + self.cube_size, gy + self.cube_size),
            (0, 0, 0),
            -1
        )

    def clear(self):
        self.canvas[:] = 0

    def merge_with_frame(self, frame):
        return cv2.add(frame, self.canvas)
