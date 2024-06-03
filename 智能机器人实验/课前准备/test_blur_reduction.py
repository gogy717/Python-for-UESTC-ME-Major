import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d, wiener
import cv2

def apply_motion_blur(image, size, angle):
    """Apply motion blur to an image."""
    kernel = np.zeros((size, size))
    kernel[int((size-1)/2), :] = np.ones(size)
    rotation_matrix = cv2.getRotationMatrix2D((size/2-0.5, size/2-0.5), angle, 1)
    kernel = cv2.warpAffine(kernel, rotation_matrix, (size, size))
    kernel = kernel / size
    return convolve2d(image, kernel, 'same')

def add_gaussian_noise(image, sigma):
    """Add Gaussian noise to an image."""
    gauss = np.random.normal(0, sigma, np.shape(image))
    noisy_image = image + gauss
    noisy_image = np.clip(noisy_image, 0, 255)  # Limit the values in the image to be between 0 and 255
    return noisy_image

def wiener_deconvolution(blurred_noisy_image, psf, balance_parameter):
    """Apply Wiener deconvolution."""
    deconvolved_image = wiener(blurred_noisy_image, psf, balance_parameter)
    return deconvolved_image

# Load an example image (grayscale)
image = plt.imread('path_to_your_image.jpg')
image = np.mean(image, axis=2)  # Convert to grayscale if necessary

# Simulate a motion blur
blurred_image = apply_motion_blur(image, size=15, angle=-30)

# Add Gaussian noise
noisy_blurred_image = add_gaussian_noise(blurred_image, sigma=10)

# Define the point spread function (PSF)
psf = np.ones((15, 15)) / 225

# Apply Wiener deconvolution
restored_image = wiener_deconvolution(noisy_blurred_image, psf, balance_parameter=0.1)

# Plot the results
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
ax[0].imshow(image, cmap='gray')
ax[0].set_title('Original Image')
ax[0].axis('off')

ax[1].imshow(noisy_blurred_image, cmap='gray')
ax[1].set_title('Blurred and Noisy Image')
ax[1].axis('off')

ax[2].imshow(restored_image, cmap='gray')
ax[2].set_title('Restored Image')
ax[2].axis('off')

plt.show()