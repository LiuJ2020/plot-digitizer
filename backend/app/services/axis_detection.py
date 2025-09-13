import cv2
import numpy as np

def detect_axes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    axes_img = img.copy()
    axes_data = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(axes_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            axes_data.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2})
    return axes_img, axes_data
