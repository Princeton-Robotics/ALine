import cv2
from siftdetector import detect_keypoints
import numpy as np

image1 = cv2.imread('hoop_images/IMG_3023.jpeg')
image2 = cv2.imread('hoop_images/IMG_3024.jpeg')

[keypoints, detectors] = detect_keypoints('hoop_images/IMG_3023.jpeg', 5)
print(keypoints)
print(detectors)

# cv2.imshow(image1)
# cv2.imshow(image2)