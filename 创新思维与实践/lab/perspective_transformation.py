import cv2
import numpy as np
import os

# 读取图像
directory = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(directory, "../images/perspective.jpeg")
# image_path = os.path.join(directory, "../images/photo.jpg")

image = cv2.imread(image_path, cv2.IMREAD_COLOR)
image = cv2.resize(image, (640, 480))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edge = cv2.Canny(gray, 160, 200, 3)

lines = cv2.HoughLinesP(edge, 1, np.pi/180, 70, minLineLength=130, maxLineGap=10)

# drop lines too close
lines = lines[np.linalg.norm(lines[:, 0, :2] - lines[:, 0, 2:], axis=1) > 100]


def draw_lines(img, lines):
    print("There are", len(lines), "lines")
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

draw_lines(img=image.copy(), lines=lines)


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

corner_points = find_corner(lines)
# drop corners out of image
corner_points = corner_points[(corner_points[:, 0] > 0) & (corner_points[:, 0] < image.shape[1]) &
                              (corner_points[:, 1] > 0) & (corner_points[:, 1] < image.shape[0])]

# drop duplicate corners
corner_points = np.unique(corner_points, axis=0)

# 过滤距离过近的角点
def remove_close_points(points, min_distance=10) -> np.ndarray:
    filtered_points = []
    for point in points:
        # 只保留与已选点距离大于min_distance的点
        if all(np.linalg.norm(point - p) > min_distance for p in filtered_points):
            filtered_points.append(point)
    return np.array(filtered_points)

corner_points = remove_close_points(corner_points)

def draw_points(img, points):
    print("There are", len(points), "points")
    for point in points:
        cv2.circle(img, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

draw_points(img=image.copy(), points=corner_points)
    
    
def sort_corners(corners: np.ndarray) -> np.ndarray:
    """
    Sort corners in order of top-left, top-right, bottom-right, bottom-left.
    
    :param corners: Detected corners, assumed to be 4 points (2D array of shape (4, 2)).
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

corner_points = sort_corners(corner_points)

dst_points = np.float32([[0, 0], [640, 0], [640, 480], [0, 480]])    
corner_points = np.float32(corner_points)
M = cv2.getPerspectiveTransform(corner_points, dst_points)
warped_image = cv2.warpPerspective(image, M, (640, 480))  # 目标图像的大小

cv2.imshow('image', warped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
    
    