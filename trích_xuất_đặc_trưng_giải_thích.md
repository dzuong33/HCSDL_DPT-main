# Giải Thích Chi Tiết Về Quá Trình Trích Xuất Đặc Trưng Ảnh Đồi Núi

Tài liệu này giải thích chi tiết cách thức hoạt động của quá trình trích xuất đặc trưng trong hệ thống nhận dạng và tìm kiếm ảnh đồi núi. Chúng tôi sẽ phân tích từng phương pháp trích xuất đặc trưng, các thư viện được sử dụng và lý do lựa chọn chúng.

## Các Thư Viện Được Sử Dụng

### 1. NumPy
- **Thư viện**: `numpy`
- **Tác dụng**: Cung cấp các cấu trúc dữ liệu mảng đa chiều và các hàm toán học để xử lý dữ liệu số. NumPy là nền tảng cho hầu hết các thao tác xử lý dữ liệu trong hệ thống.
- **Ứng dụng trong dự án**: Lưu trữ và thao tác với các vector đặc trưng, tính toán khoảng cách Euclidean, xử lý các mảng dữ liệu ảnh.

### 2. OpenCV
- **Thư viện**: `cv2` (Python interface cho OpenCV)
- **Tác dụng**: Thư viện xử lý ảnh và thị giác máy tính mã nguồn mở, cung cấp hàng trăm thuật toán xử lý ảnh.
- **Ứng dụng trong dự án**: 
  - Đọc và chuyển đổi không gian màu ảnh (RGB sang HSV, grayscale)
  - Tính toán biểu đồ màu (color histograms)
  - Phát hiện cạnh (Canny edge detection)
  - Phát hiện độ dốc (Sobel operators)
  - Phân ngưỡng ảnh (thresholding) để tách đường chân trời

### 3. scikit-image
- **Thư viện**: `skimage` 
- **Tác dụng**: Cung cấp các thuật toán xử lý ảnh nâng cao dành cho Python, tập trung vào nghiên cứu khoa học.
- **Ứng dụng trong dự án**:
  - Trích xuất đặc trưng HOG (`skimage.feature.hog`)
  - Tính toán Entropy Shannon (`skimage.measure.shannon_entropy`)

### 4. scikit-learn
- **Thư viện**: `sklearn`
- **Tác dụng**: Thư viện học máy cho Python, cung cấp các công cụ đơn giản và hiệu quả cho phân tích dữ liệu.
- **Ứng dụng trong dự án**: Chuẩn hóa các vector đặc trưng (`sklearn.preprocessing.normalize`)

### 5. Matplotlib
- **Thư viện**: `matplotlib.pyplot`
- **Tác dụng**: Thư viện vẽ đồ thị trong Python.
- **Ứng dụng trong dự án**: Trực quan hóa các đặc trưng được trích xuất và hiển thị kết quả tìm kiếm.

### 6. SciPy
- **Thư viện**: `scipy.ndimage`
- **Tác dụng**: Cung cấp các thuật toán xử lý ảnh và tín hiệu nâng cao.
- **Ứng dụng trong dự án**: Áp dụng bộ lọc đồng nhất (uniform filter) cho việc trực quan hóa entropy.

## Chi Tiết Các Phương Pháp Trích Xuất Đặc Trưng

### 1. Trích Xuất Biểu Đồ Màu Sắc (`extract_color_histogram`)

```python
def extract_color_histogram(image, bins=32):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    h_hist = cv2.calcHist([hsv], [0], None, [bins], [0, 180])
    s_hist = cv2.calcHist([hsv], [1], None, [bins], [0, 256])
    v_hist = cv2.calcHist([hsv], [2], None, [bins], [0, 256])
    
    h_hist = cv2.normalize(h_hist, h_hist, 0, 1, cv2.NORM_MINMAX)
    s_hist = cv2.normalize(s_hist, s_hist, 0, 1, cv2.NORM_MINMAX)
    v_hist = cv2.normalize(v_hist, v_hist, 0, 1, cv2.NORM_MINMAX)
    
    return np.concatenate([h_hist, s_hist, v_hist]).flatten()
```

**Giải thích chi tiết:**
1. **Chuyển đổi không gian màu**: Ảnh được chuyển từ không gian màu BGR (OpenCV mặc định) sang HSV (Hue-Saturation-Value) bằng hàm `cv2.cvtColor()`. Không gian màu HSV được lựa chọn vì:
   - Tách biệt thông tin màu sắc (Hue) khỏi cường độ sáng (Value)
   - Phù hợp hơn cho nhận dạng đặc trưng cảnh quan tự nhiên
   - Ít bị ảnh hưởng bởi điều kiện ánh sáng so với RGB

2. **Tính toán biểu đồ màu**: Sử dụng hàm `cv2.calcHist()` để tính biểu đồ phân phối màu cho mỗi kênh:
   - Kênh H (Hue): Phạm vi [0, 180] trong OpenCV (thay vì [0, 360] như thông thường)
   - Kênh S (Saturation): Phạm vi [0, 255]
   - Kênh V (Value): Phạm vi [0, 255]
   - Mỗi kênh được chia thành 32 bins (ngăn) để nắm bắt sự phân bố màu

3. **Chuẩn hóa biểu đồ**: Mỗi biểu đồ được chuẩn hóa về phạm vi [0, 1] bằng hàm `cv2.normalize()` với chế độ `cv2.NORM_MINMAX`. Điều này đảm bảo:
   - Các giá trị có thể so sánh được giữa các ảnh khác nhau
   - Giảm ảnh hưởng của kích thước ảnh và độ sáng tổng thể

4. **Tạo vector đặc trưng**: Ba biểu đồ được nối lại thành một vector duy nhất bằng `np.concatenate()` và làm phẳng (`flatten()`) thành mảng 1 chiều có 96 giá trị (32 bins × 3 kênh).

**Ý nghĩa**: Biểu đồ màu nắm bắt phân bố màu sắc trong ảnh đồi núi, giúp phân biệt các dãy núi dựa trên màu sắc đặc trưng (như núi tuyết, núi đá, núi có nhiều thực vật).

### 2. Trích Xuất Đặc Trưng Cạnh (`extract_edge_features`)

```python
def extract_edge_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    edges = cv2.Canny(gray, 100, 200)
    
    edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    orientation = np.arctan2(sobel_y, sobel_x) * (180 / np.pi) % 180
    
    hist, _ = np.histogram(orientation[magnitude > 30], bins=18, range=(0, 180), density=True)
    
    return np.concatenate([[edge_density], hist])
```

**Giải thích chi tiết:**
1. **Chuyển đổi sang ảnh xám**: Ảnh màu được chuyển sang ảnh xám bằng `cv2.cvtColor()` để đơn giản hóa quá trình xử lý.

2. **Phát hiện cạnh**: Thuật toán Canny của OpenCV (`cv2.Canny()`) được sử dụng để phát hiện cạnh trong ảnh:
   - Ngưỡng thấp (100) và ngưỡng cao (200) được chọn để phát hiện các cạnh quan trọng
   - Thuật toán Canny là phương pháp phát hiện cạnh mạnh mẽ với nhiễu thấp và phát hiện chính xác

3. **Tính mật độ cạnh**: Tỷ lệ giữa số pixel cạnh (giá trị > 0) và tổng số pixel trong ảnh:
   - Mật độ cạnh cao thường chỉ ra cảnh núi có nhiều chi tiết và đường nét phức tạp
   - Mật độ cạnh thấp có thể chỉ ra núi trơn láng hoặc có ít đường nét

4. **Tính đạo hàm theo hướng**: Toán tử Sobel (`cv2.Sobel()`) được áp dụng theo cả hai hướng x và y:
   - Sobel_x phát hiện các cạnh theo chiều dọc (gradient theo chiều ngang)
   - Sobel_y phát hiện các cạnh theo chiều ngang (gradient theo chiều dọc)
   - Kích thước kernel 3×3 (ksize=3) được sử dụng

5. **Tính độ lớn và hướng của gradient**:
   - Độ lớn được tính bằng công thức Pythagoras: `sqrt(sobel_x² + sobel_y²)`
   - Hướng được tính bằng `arctan2(sobel_y, sobel_x)` và chuyển sang độ [0, 180]

6. **Tạo biểu đồ hướng cạnh**: Chỉ xét các pixel có độ lớn gradient > 30 (lọc nhiễu) và tính phân phối hướng:
   - 18 bins cho phạm vi [0, 180] độ
   - `density=True` chuẩn hóa biểu đồ thành phân phối xác suất

7. **Tạo vector đặc trưng**: Kết hợp mật độ cạnh với biểu đồ hướng thành vector 19 chiều.

**Ý nghĩa**: Đặc trưng cạnh nắm bắt cấu trúc hình dạng của núi, đặc biệt là đường viền và sườn núi. Các hướng cạnh thường xuyên xuất hiện có thể xác định các đặc điểm như sự dốc đứng, đỉnh nhọn hoặc sườn thoai thoải.

### 3. Trích Xuất Đặc Trưng Kết Cấu (HOG) (`extract_texture_features`)

```python
def extract_texture_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    hog_features = hog(gray, orientations=9, pixels_per_cell=(16, 16),
                     cells_per_block=(2, 2), feature_vector=True)
    
    hog_features = normalize(hog_features.reshape(1, -1))[0]
    
    return hog_features
```

**Giải thích chi tiết:**
1. **Chuyển đổi sang ảnh xám**: Tương tự như trên, để đơn giản hóa quá trình xử lý.

2. **Trích xuất đặc trưng HOG**: Sử dụng hàm `hog()` từ thư viện `skimage.feature`:
   - **Orientations=9**: Chia hướng gradient thành 9 bins (khoảng), bao phủ phạm vi 0-180 độ
   - **pixels_per_cell=(16, 16)**: Mỗi cell có kích thước 16×16 pixel, đây là đơn vị cơ bản để tính biểu đồ hướng
   - **cells_per_block=(2, 2)**: Mỗi block gồm 2×2 cells, dùng để chuẩn hóa cục bộ
   - **feature_vector=True**: Trả về vector đặc trưng 1D thay vì mảng đa chiều

3. **Chuẩn hóa vector đặc trưng**: Sử dụng hàm `normalize()` từ `sklearn.preprocessing` để chuẩn hóa vector, giúp:
   - Giảm ảnh hưởng của thay đổi ánh sáng và độ tương phản
   - Cải thiện độ chính xác khi so sánh giữa các ảnh

**Nguyên lý HOG hoạt động**:
- Chia ảnh thành các cell nhỏ (16×16 pixel)
- Tính biểu đồ hướng gradient trong mỗi cell (9 bins)
- Nhóm các cell thành các block (2×2 cell) và chuẩn hóa mỗi block
- Nối các đặc trưng từ tất cả các block để tạo vector đặc trưng cuối cùng

**Ý nghĩa**: HOG đặc biệt hiệu quả trong việc nắm bắt kết cấu và hình dạng cục bộ trong ảnh. Đối với ảnh đồi núi, nó có thể phân biệt giữa các bề mặt núi (đá gồ ghề, tuyết trơn láng, thảm thực vật) và các cấu trúc như vách đá, sườn dốc, hay đỉnh núi.

### 4. Trích Xuất Đặc Trưng Đường Chân Trời (`extract_skyline_features`)

```python
def extract_skyline_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    skyline = []
    h, w = thresh.shape
    for col in range(w):
        for row in range(h):
            if thresh[row, col] < 127:  # Non-sky pixel
                skyline.append(row / h)  # Normalize by height
                break
        else:
            skyline.append(1.0)  # No skyline found in this column
    
    skyline_sampled = skyline[::w//20]  # Sample ~20 points
    
    skyline_roughness = np.std(skyline)
    
    skyline_height = np.mean(skyline)
    
    return np.concatenate([skyline_sampled, [skyline_roughness, skyline_height]])
```

**Giải thích chi tiết:**
1. **Chuyển đổi sang ảnh xám**: Như các hàm trước.

2. **Phân ngưỡng ảnh**: Sử dụng `cv2.threshold()` với phương pháp Otsu để tự động tìm ngưỡng tối ưu:
   - `THRESH_BINARY`: Chuyển ảnh thành đen trắng (0 hoặc 255)
   - `THRESH_OTSU`: Tự động xác định ngưỡng tối ưu dựa trên phân phối histogram
   - Kết quả là ảnh nhị phân phân tách bầu trời (thường sáng hơn) với phần núi (thường tối hơn)

3. **Trích xuất đường chân trời**:
   - Quét qua từng cột của ảnh
   - Tìm pixel đầu tiên không phải bầu trời (giá trị < 127) từ trên xuống
   - Lưu vị trí hàng (đã được chuẩn hóa bằng cách chia cho chiều cao) vào mảng `skyline`
   - Nếu không tìm thấy pixel núi trong cột, gán giá trị 1.0 (đáy ảnh)

4. **Lấy mẫu đường chân trời**: Giảm kích thước vector bằng cách lấy khoảng 20 điểm đại diện:
   - `skyline[::w//20]`: Lấy mỗi điểm cách nhau w//20 vị trí

5. **Tính các chỉ số đặc trưng**:
   - **Độ gồ ghề** (`skyline_roughness`): Độ lệch chuẩn của đường chân trời - chỉ ra mức độ lồi lõm/gồ ghề
   - **Chiều cao trung bình** (`skyline_height`): Vị trí trung bình của đường chân trời - chỉ ra núi chiếm bao nhiêu phần của khung hình

6. **Tạo vector đặc trưng**: Kết hợp các điểm đường chân trời với hai chỉ số trên.

**Ý nghĩa**: Đường chân trời/đường viền là đặc trưng quan trọng nhất để nhận dạng núi. Nó nắm bắt hình dạng tổng thể của núi trên nền trời - thông tin mà con người thường sử dụng để nhận biết các ngọn núi. Độ gồ ghề giúp phân biệt giữa dãy núi nhọn và núi tròn trịa, trong khi chiều cao trung bình cho biết núi chiếm bao nhiêu phần của khung hình.

### 5. Tính Toán Entropy (`compute_entropy`)

```python
def compute_entropy(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    entropy = shannon_entropy(gray)
    
    return entropy
```

**Giải thích chi tiết:**
1. **Chuyển đổi sang ảnh xám**: Như các hàm trước.

2. **Tính entropy Shannon**: Sử dụng hàm `shannon_entropy()` từ `skimage.measure`:
   - Entropy Shannon đo lường độ ngẫu nhiên hoặc độ không chắc chắn trong ảnh
   - Công thức: $H = -\sum_{i} p_i \log_2(p_i)$ với $p_i$ là xác suất xuất hiện của giá trị pixel i

**Ý nghĩa**: Entropy cao chỉ ra ảnh có nhiều chi tiết phức tạp, trong khi entropy thấp chỉ ra ảnh đơn giản, đồng nhất. Đối với ảnh đồi núi, entropy giúp phân biệt giữa các cảnh phức tạp (nhiều đỉnh, nhiều chi tiết) với cảnh đơn giản (một đỉnh núi đơn lẻ, ít chi tiết).

### 6. Trích Xuất Tất Cả Đặc Trưng (`extract_features`)

```python
def extract_features(image_path):
    image = cv2.imread(image_path)
    
    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    
    color_features = extract_color_histogram(image)
    edge_features = extract_edge_features(image)
    texture_features = extract_texture_features(image)
    skyline_features = extract_skyline_features(image)
    entropy = compute_entropy(image)
    
    features = np.concatenate([
        color_features, 
        edge_features, 
        texture_features, 
        skyline_features, 
        [entropy]
    ])
    
    return features
```

**Giải thích chi tiết:**
1. **Đọc ảnh**: Sử dụng `cv2.imread()` để đọc ảnh từ đường dẫn.

2. **Trích xuất từng loại đặc trưng**: Gọi các hàm trích xuất đặc trưng đã giải thích ở trên.

3. **Kết hợp tất cả đặc trưng**: Sử dụng `np.concatenate()` để nối tất cả vector đặc trưng thành một vector duy nhất:
   - Color features: 96 chiều (32 bins × 3 kênh)
   - Edge features: 19 chiều (1 mật độ + 18 bins hướng)
   - Texture features (HOG): ~324 chiều (phụ thuộc kích thước ảnh)
   - Skyline features: ~22 chiều (20 điểm + độ gồ ghề + chiều cao)
   - Entropy: 1 chiều

**Ý nghĩa**: Vector đặc trưng tổng hợp (~462 chiều) nắm bắt đầy đủ các khía cạnh của ảnh đồi núi: màu sắc, hình dạng, kết cấu, đường viền và độ phức tạp. Vector này sẽ được sử dụng để tính toán độ tương đồng giữa các ảnh.

### 7. Tính Khoảng Cách Euclidean (`calculate_euclidean_distance`)

```python
def calculate_euclidean_distance(features1, features2):
    return np.sqrt(np.sum((features1 - features2) ** 2))
```

**Giải thích chi tiết:**
- Khoảng cách Euclidean được tính bằng công thức: $d(p,q) = \sqrt{\sum_{i=1}^{n} (p_i - q_i)^2}$
- Trong NumPy, biểu thức `np.sqrt(np.sum((features1 - features2) ** 2))` thực hiện:
  1. Tính hiệu của hai vector đặc trưng: `(features1 - features2)`
  2. Bình phương từng phần tử: `(features1 - features2) ** 2`
  3. Tính tổng các giá trị bình phương: `np.sum(...)`
  4. Tính căn bậc hai của tổng: `np.sqrt(...)`

**Ý nghĩa**: Khoảng cách Euclidean đo lường sự khác biệt giữa hai vector đặc trưng. Khoảng cách càng nhỏ, hai ảnh càng tương tự nhau.

## Quá Trình Trực Quan Hóa Đặc Trưng

Hàm `visualize_features()` tạo ra các trực quan hóa để hiểu rõ hơn về các đặc trưng đã trích xuất:
1. **Ảnh gốc**: Hiển thị ảnh đầu vào
2. **Biểu đồ màu HSV**: Hiển thị phân phối màu trong các kênh H, S, V
3. **Phát hiện cạnh**: Hiển thị kết quả của thuật toán Canny edge detection
4. **Độ lớn gradient (HOG)**: Trực quan hóa đơn giản của đặc trưng HOG
5. **Phát hiện đường chân trời**: Hiển thị ảnh đã phân ngưỡng để phát hiện đường chân trời
6. **Entropy**: Bản đồ entropy cục bộ của ảnh

## Tổng Kết

Quá trình trích xuất đặc trưng từ ảnh đồi núi là sự kết hợp các phương pháp phân tích ảnh khác nhau để nắm bắt đầy đủ các đặc điểm:
- **Màu sắc**: Phân bố màu sắc tổng thể của cảnh núi
- **Cạnh**: Cấu trúc hình dạng và đường viền của núi
- **Kết cấu**: Chi tiết bề mặt và các mẫu địa hình
- **Đường chân trời**: Hình dạng tổng thể của núi trên nền trời
- **Entropy**: Độ phức tạp tổng thể của cảnh núi

Bằng cách kết hợp các đặc trưng này, hệ thống có thể nắm bắt đặc điểm đặc trưng của mỗi ảnh đồi núi và sử dụng khoảng cách Euclidean để tìm các ảnh tương tự nhất. Quy trình này cho phép tìm kiếm ảnh dựa trên nội dung thực tế của ảnh thay vì chỉ dựa vào metadata hoặc nhãn. 