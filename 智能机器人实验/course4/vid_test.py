import cv2
import numpy as np

lower_red = np.array([153, 32, 87])
upper_red = np.array([180, 213, 206])
lower_green = np.array([50, 20, 90])
upper_green = np.array([85, 60, 140])
cap = cv2.VideoCapture(0)
# set brightness and contrast
cap.set(10, 100)
cap.set(11, 50)


# apply reverse covolution to the image
def reverse_convolution(image, kernel):
    kernel = np.flipud(np.fliplr(kernel))
    return cv2.filter2D(image, -1, kernel)



def angle_between_lines(line1, line2):
    x1, y1, x2, y2 = line1[0]
    x3, y3, x4, y4 = line2[0]
    vector1 = [x2-x1, y2-y1]
    vector2 = [x4-x3, y4-y3]
    unit_vector1 = vector1 / np.linalg.norm(vector1)
    unit_vector2 = vector2 / np.linalg.norm(vector2)
    dot_product = np.dot(unit_vector1, unit_vector2)
    angle = np.arccos(dot_product) / np.pi * 180
    return angle


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
    # red_mask = cv2.inRange(hsv, lower_red, upper_red)
    red_mask = cv2.inRange(hsv, lower_green, upper_green)

    red_mask = reverse_convolution(red_mask, np.ones((3,3), np.uint8))  # 反卷积
    # red_mask = cv2.medianBlur(red_mask, 5)  # 中值滤波
    red_mask = cv2.GaussianBlur(red_mask, (5,5), 1)  # 使用更大的模糊核心

    red_mask = cv2.dilate(red_mask, None, iterations=6)  # 膨胀
    red_mask = cv2.erode(red_mask, None, iterations=2)  # 腐蚀
    red_mask = cv2.medianBlur(red_mask, 5)  # 中值滤波


    edges = cv2.Canny(red_mask, 100, 200)
    # draw edges
    cv2.imshow('edges', edges)
            
    #         cv2.drawContours(square_img, [approx], -1, (0, 255, 0), 3)  # 画出轮廓
    # cv2.imshow('square_img', square_img)


    # 检测圆
    red_circles = cv2.HoughCircles(edges, 
                            cv2.HOUGH_GRADIENT, 
                            dp=1, 
                            minDist=100,
                            param1=50+5,
                            param2=30+20,
                            minRadius=25,
                            maxRadius=100)
    if red_circles is not None:
        red_circles = np.uint16(np.around(red_circles))
        for i in red_circles[0, :]:
            red_center = (i[0], i[1])  # 圆心
            red_radius = i[2]          # 圆半径
            cv2.circle(frame, red_center, red_radius, (255, 0, 0), 3)  # 画圆
            cv2.circle(frame, red_center, 2, (0, 255, 0), 3)       # 画圆心
            cv2.putText(frame, f'Center: {red_center}', (red_center[0], red_center[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
    # cv2.imshow('red_mask', red_mask)
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f'Total frames read: {frame_count}')



