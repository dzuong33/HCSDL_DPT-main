# Hệ Thống Nhận Dạng Ảnh Đồi Núi

Hệ thống này trích xuất đặc trưng từ ảnh đồi núi và thực hiện tìm kiếm tương đồng để tìm các hình ảnh đồi núi tương tự về mặt trực quan.

## Tổng Quan Các Đặc Trưng

Hệ thống của chúng tôi trích xuất các đặc trưng sau từ ảnh đồi núi:
- Biểu đồ màu sắc (không gian màu HSV)
- Đặc trưng cạnh (mật độ và hướng)
- Đặc trưng kết cấu (HOG - Biểu đồ độ dốc hướng)
- Đặc trưng đường chân trời (đường viền núi)
- Entropy ảnh (đo lường độ phức tạp)

Để biết thêm chi tiết về các đặc trưng và ý nghĩa của chúng, xem [feature_description.md](./feature_description.md).

## Yêu Cầu Tiên Quyết

Hệ thống yêu cầu các gói Python sau:
```
numpy
opencv-python
scikit-image
scikit-learn
matplotlib
pandas
tqdm
```

Bạn có thể cài đặt chúng bằng:
```
pip install numpy opencv-python scikit-image scikit-learn matplotlib pandas tqdm
```

## Hướng Dẫn Sử Dụng

### 1. Trích Xuất Đặc Trưng Từ Tất Cả Ảnh

Đầu tiên, trích xuất đặc trưng từ tất cả ảnh đồi núi của bạn:

```
python extract_all_features.py 
```

Điều này sẽ:
- Xử lý tất cả ảnh trong thư mục được chỉ định
- Trích xuất vector đặc trưng cho mỗi ảnh
- Lưu các đặc trưng vào `mountain_features.pkl` và `mountain_features.csv`
- Tạo các trực quan hóa đặc trưng cho một số ảnh mẫu trong `feature_visualization/`


## Cấu Trúc Tệp

- `mountain_feature_extractor.py`: Các hàm trích xuất đặc trưng cốt lõi
- `extract_all_features.py`: Script để xử lý và lưu đặc trưng cho tất cả ảnh
- `feature_description.md`: Giải thích chi tiết về bộ đặc trưng
- `mountain_features.pkl`: Vector đặc trưng đã lưu cho tất cả ảnh (được tạo khi chạy extract_all_features.py)
- `feature_visualization/`: Thư mục chứa trực quan hóa của các đặc trưng




## Trực Quan Hóa Đặc Trưng

Đối với mỗi ảnh, chúng ta có thể trực quan hóa các khía cạnh khác nhau của quá trình trích xuất đặc trưng:
- Ảnh gốc
- Biểu đồ màu HSV
- Phát hiện cạnh
- Độ lớn của độ dốc (HOG)
- Phát hiện đường chân trời
- Bản đồ entropy

Những trực quan hóa này giúp hiểu cách hệ thống "nhìn" và phân tích các ảnh đồi núi. 