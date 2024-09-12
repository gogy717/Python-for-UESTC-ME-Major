import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import cv2
from typing import List, Tuple

from src.line_segment import *
from backlog.transformation import *
from src.vision_utils import *


def main():
    path = "images/captures/circle.png"
    # cap = cv2.VideoCapture(0)
    
    # while True:
    #     ret, frame = cap.read()
    #     cv2.imshow("frame", frame)
    #     if cv2.waitKey(1) & 0xFF == ord('c'):
    #         cv2.imwrite(path, frame)
    #         break
        
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
        
    #     cv2.imshow("frame", frame)
    #     cv2.waitKey(1)
    #     cv2.destroyAllWindows(
        
    # cap.release()
    
    line_image = image(path)
    line_image.run()
    # line_image.draw_points(line_image.targets)
    step = 10
    targets = line_image.targets
    data = {}
    for i in range(0, len(targets), step):
        data[list(targets.keys())[i]] = list(targets.values())[i]
    if len(targets) % step > step // 2:
        data[list(targets.keys())[-1]] = list(targets.values())[-1]
    line_image.draw_points(data)
    
    print(f'Debug: Targets: {line_image.targets}')






if __name__ == "__main__":
    main()
    
    print("Program finished!")

