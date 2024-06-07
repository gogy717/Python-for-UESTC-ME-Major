import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

def reverse_convolution(image, kernel):
    kernel = np.flipud(np.fliplr(kernel))
    return cv2.filter2D(image, -1, kernel)

def process_mask(mask):
    mask = reverse_convolution(mask, np.ones((3,3), np.uint8))  # 反卷积
    mask = cv2.medianBlur(mask, 5)  # 中值滤波
    mask = cv2.GaussianBlur(mask, (3,3), 1)  # 使用更大的模糊核心
    # 锐化
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    mask = cv2.filter2D(mask, -1, kernel)
    
    # mask = cv2.dilate(mask, None, iterations=6)  # 膨胀
    # mask = cv2.erode(mask, None, iterations=2)  # 腐蚀
    edges = cv2.Canny(mask, 100, 200)
    return mask,edges

def classify_circles(image, circles):
    # 遍历所有检测到的圆
    for i in circles[0, :]:
        center = (i[0], i[1])
        radius = i[2]
        red = (0,0,255)
        green = (0,255,0)
        blue = (255,0,0)
        # 提取圆的区域
        mask = np.zeros_like(image)
        cv2.circle(mask, center, radius+3, (255, 255, 255), -1)
        mask_inner = np.zeros_like(image)
        cv2.circle(mask_inner, center, radius-3, (255,255,255), -1)
        mask_ring = cv2.bitwise_xor(mask, mask_inner)
        
        circle_region = cv2.bitwise_and(image, mask_ring)
        cv2.imshow('circle_region', circle_region)
        hsv = cv2.cvtColor(circle_region, cv2.COLOR_BGR2HSV)
        lower_red = np.array([173, 50, 0])
        upper_red = np.array([180, 255, 255])
        lower_green = np.array([30, 0, 0])
        upper_green = np.array([90, 255, 255])
        lower_blue = np.array([92, 0, 0])
        upper_blue = np.array([120, 255, 255])
        
        # 计算每种颜色的像素数量
        red_count = cv2.countNonZero(cv2.inRange(hsv, lower_red, upper_red))
        green_count = cv2.countNonZero(cv2.inRange(hsv, lower_green, upper_green))
        blue_count = cv2.countNonZero(cv2.inRange(hsv, lower_blue, upper_blue))
        

        # 确定圆的颜色类别
        counts = {'red': red_count, 'green': green_count, 'blue': blue_count}
        circle_color = max(counts, key=counts.get)

        # 在原始图像上画圆和标记
        cv2.circle(image, center, radius, eval(circle_color), 3)
        cv2.circle(image, center, 2, (0, 255, 0), 3)
        cv2.putText(image, f'{circle_color} Circle', (center[0] - 50, center[1] - radius - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)


# canny
def canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 20, 80)
    return canny

while True:
    ret, frame = cap.read()
    frame = cv2.GaussianBlur(frame, (5,5), 1.1)
    frame = cv2.medianBlur(frame, 5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if not ret:
        break
    canny_image = canny(frame)
    # canny_image = cv2.dilate(canny_image, None, iterations=4)
    # canny_image = cv2.erode(canny_image, None, iterations=5)
    circles = cv2.HoughCircles(canny_image, 
                            cv2.HOUGH_GRADIENT, 
                            dp=1, 
                            minDist=100,
                            param1=50+5,
                            param2=30+0,
                            minRadius=180,
                            maxRadius=200)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        classify_circles(frame, circles)
        
    cv2.imshow("canny", canny_image)
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
