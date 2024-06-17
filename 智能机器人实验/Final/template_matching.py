import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(__file__))
os.chdir('..')


def detect_and_match_features(img1, img2, feature_method='SIFT'):
    """
    Detect and match features between two images using SIFT or SURF.

    Args:
        img1 (numpy.ndarray): First image.
        img2 (numpy.ndarray): Second image.
        feature_method (str): Method to use, 'SIFT' or 'SURF'.

    Returns:
        img_matches (numpy.ndarray): Image showing matches.
    """
    # Initialize detector
    if feature_method == 'SIFT':
        detector = cv2.SIFT_create()
    elif feature_method == 'SURF':
        detector = cv2.xfeatures2d.SURF_create(400)
    else:
        raise ValueError("Invalid method specified. Use 'SIFT' or 'SURF'.")

    # Detect keypoints and descriptors
    kp1, des1 = detector.detectAndCompute(img1, None)
    kp2, des2 = detector.detectAndCompute(img2, None)

    # Match descriptors
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Draw matches
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    return img_matches

# 1. load imgs
img = cv2.imread('IMG_0014.jpg',0)

# 2.load template
template = cv2.imread('image.jpg',0)

# 3. detect and match
img_matches = detect_and_match_features(template,img,feature_method='SIFT')

# Display the matches
plt.figure(figsize=(12, 6))
plt.imshow(img_matches)
plt.axis('off')
plt.show()