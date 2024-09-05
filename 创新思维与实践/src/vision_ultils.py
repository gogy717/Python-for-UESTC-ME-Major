import cv2
import numpy as np
from typing import List, Tuple

def get_image(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (640, 480))
    image = cv2.GaussianBlur(image, (5, 5), 0)
    return image


def get_gray(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray


def draw_lines(img: np.ndarray, lines: List[Tuple[int, int, int, int]]) -> None:
    """
    draw lines on image
    :param img: image
    :param lines: lines detected by HoughLinesP
    """
    
    print("There are", len(lines), "lines")
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

def draw_points(img, points):
    print("There are", len(points), "points")
    for point in points:
        cv2.circle(img, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




