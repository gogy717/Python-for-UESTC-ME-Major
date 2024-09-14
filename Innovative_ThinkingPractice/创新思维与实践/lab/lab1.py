import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


# 读取图像

image_path = "../images/line.jpg"
dir_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(dir_path, image_path)
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 转换为二值图像
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

# 细化图像，找到骨架
skeleton = cv2.ximgproc.thinning(binary, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)

# 显示结果
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title('Original Binary Image')
plt.imshow(binary, cmap='gray')

plt.subplot(1, 2, 2)
plt.title('Skeleton')
plt.imshow(skeleton, cmap='gray')
plt.show()






