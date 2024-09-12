import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import cv2
from typing import List, Tuple

from src.line_segment import *
from src.transformation import *
from src.vision_utils import *


def main():
    # Open serial port
    # ser = serial.Serial('COM3', 9600, timeout=1)

    # Open the camera
    ## load image instead while testing
    # path = 'images/captures/frame1.png'
    # file_path = "/Users/luozhufeng/Desktop/Python-for-UESTC-ME-Major/创新思维与实践/images/captures/frame2.png"
    # image = get_image(file_path)
    # gray = get_gray(image)
    # edges = get_edges(gray)
    # paper = find_paper(edges)
    
    # image = cv2.imread(file_path)
    # image = cv2.resize(image, (640, 360))
    
    # mapped_paper = map_a4_paper(paper, image)
    
    # cv2.imshow('mapped_paper', mapped_paper)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # mapped_paper = get_gray(mapped_paper)
    # cv2.imwrite('images/captures/mapped_paper.png', mapped_paper)
    # targets = get_all_targets(image)
    # print(f'Debug: Targets: {targets}')
    
    # draw_points(image, targets)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.destroyAllWindows()

            image = get_image('images/line.jpg')
            gray = get_gray(frame)
            targets = get_all_targets(gray)
            print(f'Debug: Targets: {targets}')
            draw_points(image, targets)
        
    cap.release()
    





if __name__ == "__main__":
    main()
    
    print("Program finished!")

