import os
import numpy as np
import cv2
from skimage.feature import hog
from utils import resize_image, get_hog_feature, get_hoc_feature

# Cấu hình thư mục
IMAGE_DIR = 'assignment/mountain_images'
META_DIR = 'assignment/meta'
os.makedirs(META_DIR, exist_ok=True)

# Các hàm xử lý đặc trưng
def resize_image(image, size=(96, 96)):
    return cv2.resize(image, size)

def get_hog_feature(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return hog(gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm='L2-Hys', feature_vector=True)

def get_hoc_feature(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 3, 3], [0, 180, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

# Danh sách đặc trưng
hog_features = []
hoc_features = []
labels = []

# Duyệt ảnh
for filename in os.listdir(IMAGE_DIR):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(IMAGE_DIR, filename)
        image = cv2.imread(path)
        if image is None:
            continue

        image_resized = resize_image(image)
        hog_vec = get_hog_feature(image_resized)
        hoc_vec = get_hoc_feature(image_resized)

        hog_features.append(hog_vec)
        hoc_features.append(hoc_vec)
        labels.append(filename)

# Lưu vector đặc trưng
np.save(os.path.join(META_DIR, 'hog_features.npy'), np.array(hog_features))
np.save(os.path.join(META_DIR, 'hoc_features.npy'), np.array(hoc_features))
np.save(os.path.join(META_DIR, 'labels.npy'), np.array(labels))

print("✅ Đã trích xuất và lưu đặc trưng")
