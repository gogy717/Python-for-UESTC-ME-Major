import cv2
import numpy as np

# 打开摄像头
cap = cv2.VideoCapture(1)  # 0表示使用默认摄像头

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    # 从摄像头捕获帧
    ret, frame = cap.read()
    if not ret:
        print("no frame")
        break
    
    # 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 转换为二值图像
    _, binary = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY_INV)
    
    # 使用 Zhang-Suen 算法细化图像
    skeleton = cv2.ximgproc.thinning(binary, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    
    # 显示原始图像和骨架化图像
    cv2.imshow('Original', frame)
    cv2.imshow('Skeleton', skeleton)
    
    # 按 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源并关闭窗口
cap.release()
cv2.destroyAllWindows()


