import cv2
import numpy as np
from typing import List, Tuple
from vision_ultils import *


def get_skeleton(gray: np.ndarray) -> np.ndarray:
    # 转换为二值图像
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                cv2.THRESH_BINARY_INV, 11, 2)
    # 二值图像的是否全空
    if cv2.countNonZero(binary) == 0:
        print('二值图像全空')

    # 细化图像，找到骨架
    skeleton = cv2.ximgproc.thinning(binary, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    return skeleton


def skeleton_endpoints(skel: np.ndarray) -> np.ndarray:
    """
    Finds the endpoints in a skeleton image.

    Parameters:
    skel (ndarray): The input skeleton image.

    Returns:
    ndarray: An array containing the coordinates of the endpoints.
    """
    # Rest of the code...
    # Make our input nice, possibly necessary.
    skel = skel.copy()
    skel[skel!=0] = 1
    skel = np.uint8(skel)

    # Apply the convolution.
    kernel = np.uint8([[1,  1, 1],
                       [1, 10, 1],
                       [1,  1, 1]])
    src_depth = -1
    filtered = cv2.filter2D(skel,src_depth,kernel)

    # Look through to find the value of 11.
    # This returns a mask of the endpoints, but if you
    # just want the coordinates, you could simply
    # return np.where(filtered==11)
    out = np.zeros_like(skel)
    out[np.where(filtered==11)] = 1
    out = np.argwhere(out > 0)
    return out


def bfs(skeleton: np.ndarray, start: tuple, end: tuple) -> list:
    """
    Perform breadth-first search (BFS) algorithm to find the shortest path from the start point to the end point in a skeleton.
    Parameters:
    - skeleton (numpy.ndarray): The skeleton image represented as a 2D numpy array.
    - start (tuple): The starting point coordinates (x, y) in the skeleton.
    - end (tuple): The ending point coordinates (x, y) in the skeleton.
    Returns:
    - list: The shortest path from the start point to the end point as a list of coordinates [(x1, y1), (x2, y2), ...].
           If no path is found, an empty list is returned.
    """
    # 定义 8 邻域
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    # 队列初始化，存储当前位置和路径
    queue = deque([(start, [start])])
    
    # 访问过的节点
    visited = np.zeros(skeleton.shape, dtype=np.uint8)
    visited[start] = 1
    
    while queue:
        (x, y), path = queue.popleft()
        
        # 如果找到目标端点，返回路径
        if (x, y) == end:
            return path
        
        # 遍历 8 邻域
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # 确保新位置在图像范围内并且是骨架的一部分且未访问
            if 0 <= nx < skeleton.shape[0] and 0 <= ny < skeleton.shape[1] and skeleton[nx, ny] == 255 and not visited[nx, ny]:
                visited[nx, ny] = 1
                queue.append(((nx, ny), path + [(nx, ny)]))  # 将路径延展
    
    # 如果无法到达，返回空路径
    return []


def get_path_derivative(path: list, step: int = 10) -> dict:
    """
    Calculate the derivative of a path represented as a list of coordinates [(x1, y1), (x2, y2), ...].
    
    Parameters:
    - path (list): The input path as a list of coordinates [(x1, y1), (x2, y2), ...].
    - step (int): The step size for calculating the derivative (default: 10).
    
    Returns:
    - dict: A dictionary where the keys are points from the path and the values are the calculated derivatives.
    """
    # 提前检查路径点的数量是否足够进行拟合
    if 2 * len(path) < 3:
        raise ValueError("The path is too short for quadratic fitting (requires at least 3 points).")

    derivatives = {}
    
    for i in range(step, len(path), step):
        # 处理边界问题，确保不会超出路径范围
        start_idx = max(0, i - step)
        end_idx = min(len(path), i + step)
        
        # 提取邻近点
        x = np.array([p[0] for p in path[start_idx:end_idx]])
        y = np.array([p[1] for p in path[start_idx:end_idx]])

        # 使用二次多项式拟合
        z = np.polyfit(x, y, 2)  # z[1] 是一次项的系数，即斜率
        
        # 对拟合的多项式求导：f'(x) = 2 * z[0] * x + z[1]
        current_x = path[i][0]
        slope = 2 * z[0] * current_x + z[1]
        
        # 存储当前点的斜率
        derivatives[path[i]] = slope
        
    return derivatives




