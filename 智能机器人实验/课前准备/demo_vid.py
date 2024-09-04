import cv2
import numpy as np
# video_path = "/Users/luozhufeng/Desktop/Python-for-UESTC-ME-Major/智能机器人实验/课前准备/IMG_0013.mp4"
video_path = "/Users/luozhufeng/Desktop/Python-for-UESTC-ME-Major/智能机器人实验/课前准备/output.mp4"
lower_red = np.array([153, 32, 87])
upper_red = np.array([180, 213, 206])
lower_green = np.array([50, 13, 16])
upper_green = np.array([94, 84, 134])
lower_blue = np.array([92, 40, 40])
upper_blue = np.array([120, 255, 200])
lower_green1 = np.array([40, 6, 0])
upper_green1 = np.array([97, 85, 130])
cap = cv2.VideoCapture(0)

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

# apply reverse covolution to the image
def reverse_convolution(image, kernel):
    kernel = np.flipud(np.fliplr(kernel))
    return cv2.filter2D(image, -1, kernel)

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
    # Read the image
    if img is None:
        raise ValueError("Image not found at the specified path.")

    
    # Create a CLAHE object
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    
    # Apply CLAHE
    enhanced_img = clahe.apply(img)
    
    return enhanced_img

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 分离 HSV 通道
    h, s, v = cv2.split(hsv)

    # 对 V 通道应用中值滤波
    v = apply_CLAHE(v)
    v_filtered = cv2.medianBlur(v, 3)  # 5 是核大小，可以根据需要调整

    # 重新组合 HSV 通道
    hsv = cv2.merge([h, s, v_filtered])
    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    
    green_mask1 = cv2.inRange(hsv, lower_green1, upper_green1)
    red_mask_inv = cv2.bitwise_not(red_mask)
    red_mask_inv = cv2.erode(red_mask_inv, None, iterations=4)
    blue_mask_inv = cv2.bitwise_not(blue_mask)
    blue_mask_inv = cv2.erode(blue_mask_inv, None, iterations=4)
    green_mask = cv2.bitwise_and(red_mask_inv, green_mask1)
    green_mask = cv2.bitwise_and(green_mask, blue_mask_inv)
    green_mask = cv2.medianBlur(green_mask, 5)
    
    red_mask,red_edges = process_mask(red_mask)
    blue_mask,blue_edges = process_mask(blue_mask)
    green_mask,green_edges = process_mask(green_mask)
    
    all_edges = cv2.bitwise_xor(red_edges, blue_edges)
    all_edges = cv2.bitwise_xor(all_edges, green_edges)
    # 检测圆
    red_circles = cv2.HoughCircles(red_edges, 
                            cv2.HOUGH_GRADIENT, 
                            dp=1, 
                            minDist=100,
                            param1=50+5,
                            param2=30+0,
                            minRadius=180,
                            maxRadius=200)
    blue_circles = cv2.HoughCircles(blue_edges,
                            cv2.HOUGH_GRADIENT, 
                            dp=1, 
                            minDist=100,
                            param1=50+5,
                            param2=30+0,
                            minRadius=180,
                            maxRadius=200)
    green_circles = cv2.HoughCircles(green_edges,
                            cv2.HOUGH_GRADIENT, 
                            dp=1, 
                            minDist=100,
                            param1=50+5,
                            param2=30+0,
                            minRadius=180,
                            maxRadius=200)
    
    if red_circles is not None:
        red_circles = np.uint16(np.around(red_circles))
        for i in red_circles[0, :]:
            red_center = (i[0], i[1])  # 圆心
            red_radius = i[2]          # 圆半径
            cv2.circle(frame, red_center, red_radius, (0, 0, 255), 3)  # 画圆
            cv2.circle(frame, red_center, 2, (0, 255, 0), 3)       # 画圆心
            cv2.putText(frame, f'Center: {red_center},Radius: {red_radius}', (red_center[0], red_center[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    if blue_circles is not None:
        blue_circles = np.uint16(np.around(blue_circles))
        for i in blue_circles[0, :]:
            blue_center = (i[0], i[1])
            blue_radius = i[2]
            cv2.circle(frame, blue_center, blue_radius, (255, 0, 0), 3)
            cv2.circle(frame, blue_center, 2, (0, 255, 0), 3)
            cv2.putText(frame, f'Center: {blue_center},Radius: {blue_radius}', (blue_center[0], blue_center[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    if green_circles is not None:
        green_circles = np.uint16(np.around(green_circles))
        for i in green_circles[0, :]:
            green_center = (i[0], i[1])
            green_radius = i[2]
            cv2.circle(frame, green_center, green_radius, (0, 255, 0), 3)
            cv2.circle(frame, green_center, 2, (0, 255, 0), 3)
            cv2.putText(frame, f'Center: {green_center},Radius: {green_radius}', (green_center[0], green_center[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
            
    # cv2.imshow('red_mask', red_mask)
    
    cv2.imshow('greenmask', green_mask)
    cv2.imshow('bluemask', blue_mask)
    cv2.imshow('redmask', red_mask)
    
    # cv2.imshow('edges', all_edges)
    cv2.imshow('Frame', frame)

                
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f'Total frames read: {frame_count}')



