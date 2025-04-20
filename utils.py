import numpy as np
import cv2
from skimage.feature import hog

# Cấu hình HOG
HOG_PARAMS = {
    "orientations": 9,
    "pixels_per_cell": (8, 8),
    "cells_per_block": (2, 2),
    "block_norm": 'L2-Hys',
    "feature_vector": True
}

# Hàm resize ảnh
def resize_image(image, size=(96, 96)):
    return cv2.resize(image, size)

# Hàm trích xuất đặc trưng HOG
def get_hog_feature(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_resized = resize_image(gray, size=(96, 96))  # Resize ảnh về kích thước cố định
    # Trích xuất đặc trưng HOG từ ảnh đã resize
    fd = hog(image_resized, **HOG_PARAMS)
    return fd

# Hàm trích xuất đặc trưng HOC
def get_hoc_feature(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 3, 3],
                        [0, 180, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

# Hàm tính khoảng cách Euclidean
def euclidean_distance(a, b):
    return np.linalg.norm(a - b)
