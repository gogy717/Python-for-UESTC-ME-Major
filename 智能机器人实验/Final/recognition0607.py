import cv2
import numpy as np
import time
video_path = '/Users/luozhufeng/Desktop/Python-for-UESTC-ME-Major/智能机器人实验/IMG_0021.mp4'
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)  # 设置自动曝光
# cap.set(cv2.CAP_PROP_EXPOSURE, -100)  # 设置曝光
def apply_CLAHE(img, clip_limit=2.0, tile_grid_size=(8, 8)):
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE) to an image.

    Parameters:
        image_path (str): Path to the input image.
        clip_limit (float): Threshold for contrast limiting. Higher values increase contrast.
        tile_grid_size (tuple): Size of the grid for the tiles used to compute the histogram.

    Returns:
        output_image (numpy.ndarray): Image after applying CLAHE.
    """
    # Read the imagex
    if img is None:
        raise ValueError("Image not found at the specified path.")

    
    # Create a CLAHE object
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    
    # Apply CLAHE
    enhanced_img = clahe.apply(img)
    
    return enhanced_img

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
        upper_green = np.array([90, 150, 255])
        lower_blue = np.array([92, 40, 40])
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
    canny = cv2.Canny(blur, 10, 50)
    return canny

while True:
    ret, frame = cap.read()
    print(frame.shape)
    frame = cv2.GaussianBlur(frame, (5,5), 1.1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    v_filtered = apply_CLAHE(v)
    # hsv = cv2.merge([h, s, v_filtered])
    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    frame = cv2.GaussianBlur(frame, (5,5), 1.1)
    # frame = cv2.medianBlur(frame, 5)
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
                            param2=30+40,
                            minRadius=100,
                            maxRadius=200)
    if circles is None:
        print('No circles detected.')
        circles = cv2.HoughCircles(canny_image,
                        cv2.HOUGH_GRADIENT, 
                        dp=1, 
                        minDist=100,
                        param1=50+5,
                        param2=30+45,
                        minRadius =50,
                        maxRadius=100)
    if circles is not None:
        # print(circles)
        circles = np.uint16(np.around(circles))
        classify_circles(frame, circles)
        
    canny_v = cv2.Canny(v, 10, 200)
    cv2.imshow('canny_v', canny_v)
    dots = cv2.HoughCircles(canny_image,
                           cv2.HOUGH_GRADIENT,
                            dp=1,
                            minDist=100,
                            param1=25,
                            param2=20,
                            minRadius=3,
                            maxRadius=10)
    # draw dots 
    if dots is not None:
        dots = np.uint16(np.around(dots))
        for i in dots[0, :]:
            center = (i[0], i[1])
            cv2.circle(frame, center, 2, (0, 0, 255), 3)
            
    cv2.imshow("canny", canny_image)
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
