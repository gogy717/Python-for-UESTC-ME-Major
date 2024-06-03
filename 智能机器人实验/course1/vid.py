import cv2
import numpy as np
import matplotlib.pyplot as plt


# read image
img = cv2.imread('/Users/luozhufeng/Desktop/Python-for-UESTC-ME-Major/智能机器人实验/course1/IMG_0014.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.axis('off')  # 关闭坐标轴
plt.show()
# 打开摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # 从摄像头读取一帧
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read from camera.")
        break

    # 显示原始帧
    # downsize the frame 1/2
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow('Original Frame', frame)

    # 分离 B, G, R 通道
    b, g, r = cv2.split(frame)
    
    # 创建纯黑色图像以显示单个颜色通道
    zero_channel = np.zeros_like(b)

    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Gray Image', gray_image)
    # 只显示红色通道
    r_image = cv2.merge([zero_channel, zero_channel, r])
    cv2.imshow('Red Channel', r_image)
    
    # 只显示绿色通道
    g_image = cv2.merge([zero_channel, g, zero_channel])
    cv2.imshow('Green Channel', g_image)
    
    # 只显示蓝色通道
    b_image = cv2.merge([b, zero_channel, zero_channel])

    cv2.imshow('Blue Channel', b_image)

    # 按 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()
# 关闭所有 OpenCV 窗口
cv2.destroyAllWindows()