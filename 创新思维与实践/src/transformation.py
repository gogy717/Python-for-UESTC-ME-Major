import cv2
import numpy as np
from typing import List, Tuple
from vision_utils import *

def find_lines(image: np.ndarray, min_line_length: int = 100) -> np.ndarray:
    """
    Find lines in an image using the Hough transform.
    
    :param image: Input image.
    :param min_line_length: Minimum length of a line to be detected.
    :return: Detected lines.
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Apply Hough transform to detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 70, minLineLength=130, maxLineGap=10)

    # drop lines too close
    lines = lines[np.linalg.norm(lines[:, 0, :2] - lines[:, 0, 2:], axis=1) > 100]
    
    return lines


def find_corner(lines: np.ndarray) -> np.ndarray:
    """
    find all cross points of lines
    :param lines: lines detected by HoughLinesP
    
    :return: cross points
    """
    def get_line_equation(line: np.ndarray) -> np.ndarray:
        """
        get line equation from two points
        :param line: two points of line
        
        :return: line equation
        """
        x1, y1, x2, y2 = line
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
        return np.array([k, b])
    
    def get_cross_point(line1: np.ndarray, line2: np.ndarray) -> np.ndarray:
        """
        get cross point of two lines
        :param line1: line equation
        :param line2: line equation
        
        :return: cross point
        """
        k1, b1 = line1
        k2, b2 = line2
        x = (b2 - b1) / (k1 - k2)
        y = k1 * x + b1
        return np.array([x, y])
    
    cross_points = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            line1 = get_line_equation(lines[i][0])
            line2 = get_line_equation(lines[j][0])
            cross_points.append(get_cross_point(line1, line2))
    
    return np.array(cross_points)


def remove_outliers(points, threshold):
    """
    Remove outliers from a set of points based on a distance threshold.
    
    :param points: Array of points.
    :param threshold: Maximum distance allowed for a point to be considered an outlier.
    :return: Array of points without outliers.
    """
    filtered_points = []
    for point in points:
        # Calculate the distance between the point and the centroid
        distance = np.linalg.norm(point - np.mean(points, axis=0))
        # Only keep points that are within the threshold distance
        if distance <= threshold:
            filtered_points.append(point)
    return np.array(filtered_points)


def remove_close_points(points, min_distance=10) -> np.ndarray:
    """
    Remove points that are too close to each other.
    """
    filtered_points = []
    for point in points:
        # 只保留与已选点距离大于min_distance的点
        if all(np.linalg.norm(point - p) > min_distance for p in filtered_points):
            filtered_points.append(point)
    return np.array(filtered_points)


def sort_corners(corners: np.ndarray) -> np.ndarray:
    """
    Sort corners in order of top-left, top-right, bottom-right, bottom-left.
    
    :param : Detected corners, assumed to be 4 points (2D array of shape (4, 2)).
    :return: Sorted corners (in top-left, top-right, bottom-right, bottom-left order).
    """
    # Calculate the centroid of the corners
    center = np.mean(corners, axis=0)

    # Calculate the angle of each point with respect to the centroid
    angles = np.arctan2(corners[:, 1] - center[1], corners[:, 0] - center[0])

    # Sort the corners by angle (clockwise order starting from top-left)
    sorted_indices = np.argsort(angles)

    # Rearrange the corners in the desired order (top-left, top-right, bottom-right, bottom-left)
    sorted_corners = corners[sorted_indices]

    return sorted_corners


def perspective_transform(image: np.ndarray, corner_points: np.ndarray, imshow: bool = False) -> np.ndarray:
    """
    Perform perspective transformation on an image using the given corner points.
    
    :param image: Input image.
    :param corner_points: Corner points of the region of interest.
    :return: Warped image.
    """
    
    dst_points = np.float32([[0, 0], [640, 0], [640, 480], [0, 480]])    
    corner_points = np.float32(corner_points)
    M = cv2.getPerspectiveTransform(corner_points, dst_points)
    warped_image = cv2.warpPerspective(image, M, (640, 480))  # 目标图像的大小
    
    if imshow:
        cv2.imshow('image', warped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return warped_image
    
def get_warped_image(image: np.ndarray) -> np.ndarray:
    """
    Get warped image
    
    :param image: input image
    
    :return: warped image
    """
    lines = find_lines(image)
    corner_points = find_corner(lines)
    # corner_points = remove_outliers(corner_points, 100)
    corner_points = remove_close_points(corner_points)
    corner_points = sort_corners(corner_points)
    return perspective_transform(image, corner_points)

if __name__ == "__main__":
    image = get_image("images/captures/frame0.png")
    warped = get_warped_image(image)
    cv2.imshow('image', warped)