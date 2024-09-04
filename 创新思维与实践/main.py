import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import cv2


def main():
    # Open serial port
    ser = serial.Serial('COM3', 9600, timeout=1)

    # Create a figure and a set of subplots
    fig, ax = plt.subplots()




