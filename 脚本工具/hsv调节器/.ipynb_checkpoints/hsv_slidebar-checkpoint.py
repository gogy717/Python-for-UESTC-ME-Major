import cv2
import numpy as np

def nothing(x):
    pass

# 创建一个窗口
cv2.namedWindow("Trackbars")

# 创建滑动条，用于调整HSV范围
cv2.createTrackbar("LH", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("LS", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("LV", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("UH", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("US", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("UV", "Trackbars", 255, 255, nothing)

# 打开摄像头
cap = cv2.VideoCapture(0)


while True:
    # 读取摄像头的一帧
    ret, frame = cap.read()
    if not ret:
        break

    # 转换到HSV色彩空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 从滑动条获取当前的HSV阈值
    l_h = cv2.getTrackbarPos("LH", "Trackbars")
    l_s = cv2.getTrackbarPos("LS", "Trackbars")
    l_v = cv2.getTrackbarPos("LV", "Trackbars")
    u_h = cv2.getTrackbarPos("UH", "Trackbars")
    u_s = cv2.getTrackbarPos("US", "Trackbars")
    u_v = cv2.getTrackbarPos("UV", "Trackbars")

    # 创建HSV阈值范围的掩码
    lower_hsv = np.array([l_h, l_s, l_v])
    upper_hsv = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # 将掩码与原图做位运算，只显示指定颜色范围
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # 显示结果图
    cv2.imshow("Result", result)

    # 按'ESC'键退出
    key = cv2.waitKey(1)
    if key == 27:
        break

# 释放摄像头资源并销毁所有窗口
cv2.destroyAllWindows()
print(f'lower_hsv: {lower_hsv}')
print(f'upper_hsv: {upper_hsv}')