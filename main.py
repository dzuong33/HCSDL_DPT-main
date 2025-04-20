import numpy as np
import cv2
import os
from utils import resize_image, get_hog_feature, get_hoc_feature, euclidean_distance

# Load đặc trưng và labels từ thư mục assignment/meta/
hog_features = np.load('assignment/meta/hog_features.npy')
hoc_features = np.load('assignment/meta/hoc_features.npy')
labels = np.load('assignment/meta/labels.npy')

# Kiểm tra kích thước của hog và hoc features
print(f"hog_features.shape: {hog_features.shape}")
print(f"hoc_features.shape: {hoc_features.shape}")

# Đọc ảnh truy vấn
query_image_path = 'test/test4.jpg'  # Đặt ảnh truy vấn tại thư mục gốc
if not os.path.exists(query_image_path):
    raise FileNotFoundError("⚠️ Không tìm thấy ảnh query.jpg!")

query_image = cv2.imread(query_image_path)
query_image_resized = resize_image(query_image, size=(96, 96))  # Resize ảnh truy vấn
query_hog = get_hog_feature(query_image_resized)  # Trích xuất đặc trưng HOG
query_hoc = get_hoc_feature(query_image_resized)

# Đảm bảo rằng kích thước của query_hog khớp với kích thước của hog_features
if query_hog.shape[0] != hog_features.shape[1]:
    print(f"⚠️ Kích thước không khớp: query_hog: {query_hog.shape[0]}, hog_features: {hog_features.shape[1]}")
    # Có thể cần phải thực hiện một số điều chỉnh trong hàm `get_hog_feature` để đảm bảo kích thước đồng nhất

# Sau khi điều chỉnh kích thước, tiến hành tính khoảng cách
distances = []
for hog, hoc in zip(hog_features, hoc_features):
    dist = euclidean_distance(query_hog, hog) + euclidean_distance(query_hoc, hoc)
    distances.append(dist)

# Kiểm tra kích thước của các đặc trưng truy vấn
print(f"query_hog.shape: {query_hog.shape}")
print(f"query_hoc.shape: {query_hoc.shape}")

# Tính khoảng cách kết hợp HOG + HOC
distances = []
for hog, hoc in zip(hog_features, hoc_features):
    # Kiểm tra kích thước trước khi tính khoảng cách
    if hog.shape != query_hog.shape or hoc.shape != query_hoc.shape:
        print(f"⚠️ Kích thước không khớp: hog: {hog.shape}, query_hog: {query_hog.shape}, hoc: {hoc.shape}, query_hoc: {query_hoc.shape}")
        continue
    dist = euclidean_distance(query_hog, hog) + euclidean_distance(query_hoc, hoc)
    distances.append(dist)

# Lấy 3 ảnh gần nhất
top_indices = np.argsort(distances)[:3]

print("🔍 Top 3 ảnh giống nhất với ảnh truy vấn:")
for rank, idx in enumerate(top_indices, 1):
    print(f"{rank}. {labels[idx]} (distance = {distances[idx]:.2f})")
