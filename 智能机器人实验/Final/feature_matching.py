import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import os

os.chdir(os.path.dirname(__file__))
os.chdir('..')

def extract_strong_features(img, method='sift', top_k=80):
    """
    Extract strong features from the image using the specified method.

    Args:
        img (numpy.ndarray): Input image.
        method (str): Feature extraction method to use. Can be 'sift' or 'surf'.
        top_k (int): Number of top keypoints to retain based on response.

    Returns:
        kp (list): List of keypoints.
        des (numpy.ndarray): Descriptors corresponding to the keypoints.
    """
    if method == 'sift':
        detector = cv2.SIFT_create()
    elif method == 'surf':
        detector = cv2.xfeatures2d.SURF_create()
    else:
        raise ValueError("Invalid method specified. Use 'sift' or 'surf'.")

    kp, des = detector.detectAndCompute(img, None)
    kp = sorted(kp, key=lambda x: -x.response)[:top_k]

    return kp, np.array([des[i] for i in range(len(kp))])

def feature_matching(img1, img2, kp1, des1, method='sift'):
    """
    Perform feature matching between two images using the specified method.

    Args:
        img1 (numpy.ndarray): First image.
        img2 (numpy.ndarray): Second image.
        kp1 (list): List of keypoints in the first image.
        des1 (numpy.ndarray): Descriptors corresponding to keypoints in the first image.
        method (str): Feature matching method to use. Can be 'sift' or 'surf'.

    Returns:
        kp2 (list): List of keypoints in the second image.
        good_matches (list): List of good matched keypoints.
    """
    if method == 'sift':
        detector = cv2.SIFT_create()
    elif method == 'surf':
        detector = cv2.xfeatures2d.SURF_create()
    else:
        raise ValueError("Invalid method specified. Use 'sift' or 'surf'.")

    kp2, des2 = detector.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    return kp2, good_matches

def draw_matches(img1, img2, kp1, kp2, matches):
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    plt.figure(figsize=(12, 6))
    plt.imshow(img_matches)
    plt.axis('off')
    plt.show()

def cluster_keypoints(kp2, matches):
    points = np.float32([kp2[m.trainIdx].pt for m in matches])
    clustering = DBSCAN(eps=30, min_samples=2).fit(points)
    labels = clustering.labels_
    unique_labels = set(labels)
    clusters = {label: [] for label in unique_labels if label != -1}
    
    for label, match in zip(labels, matches):
        if label != -1:
            clusters[label].append(match)
    
    return clusters

def find_homography_and_draw_clusters(img1, img2, kp1, kp2, clusters, min_match_count=10):
    h, w = img1.shape[:2]
    img2_with_boxes = img2.copy()
    
    for label, matches in clusters.items():
        if len(matches) > min_match_count:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 2)
            
            # Calculate convex hull for each cluster
            hull = cv2.convexHull(dst_pts)
            
            # Draw the convex hull on the image
            img2_with_boxes = cv2.polylines(img2_with_boxes, [np.int32(hull)], True, (0, 255, 0), 3, cv2.LINE_AA)
    
    plt.figure(figsize=(12, 6))
    plt.imshow(cv2.cvtColor(img2_with_boxes, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

# Load the images
img1 = cv2.imread('image.jpg')
img2 = cv2.imread('IMG_0014.jpg')

# Check if images are loaded successfully
if img1 is None or img2 is None:
    raise IOError("Error loading images. Please check the file paths.")

# Add Gaussian blur to the images
img1 = cv2.GaussianBlur(img1, (5, 5), 1)
img2 =  cv2.GaussianBlur(img2, (5, 5), 1)

# Convert the images to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Extract strong features from the first image
kp1, des1 = extract_strong_features(gray1, method='sift', top_k=50)

# Perform feature matching
kp2, matches = feature_matching(gray1, gray2, kp1, des1, method='sift')

# Draw the matches (optional, for visualization)
draw_matches(img1, img2, kp1, kp2, matches)

# Cluster keypoints in the second image
clusters = cluster_keypoints(kp2, matches)

# Find homography and draw the detected objects for each cluster
find_homography_and_draw_clusters(img1, img2, kp1, kp2, clusters)
