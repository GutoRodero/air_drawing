import math

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def finger_touching_thumb(thumb, finger, threshold=40):
    return distance(thumb, finger) < threshold
