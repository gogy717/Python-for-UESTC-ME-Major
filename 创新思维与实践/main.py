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
    path = 'images/captures/frame1.png'
    image = get_image(path)
    
    gray = get_gray(image)
    
    wrapped = get_warpped_image(image)
    
    targets = get_all_targets(wrapped)
    print(f'Debug: Targets: {targets}')
    
    draw_points(wrapped, targets)
    





if __name__ == "__main__":
    main()
    
    print("Program finished!")

