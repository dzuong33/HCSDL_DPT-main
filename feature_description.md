# Hệ Thống Trích Xuất và Nhận Dạng Đặc Trưng Ảnh Đồi Núi

Tài liệu này mô tả bộ đặc trưng được thiết kế để nhận dạng ảnh đồi núi từ bộ dữ liệu gồm 100 ảnh đồi núi. Các đặc trưng được lựa chọn cẩn thận để nắm bắt các đặc điểm độc đáo của đồi núi và cho phép tìm kiếm tương đồng chính xác.

## Mô Tả Bộ Đặc Trưng

Hệ thống trích xuất đặc trưng của chúng tôi trích xuất các loại đặc trưng sau từ ảnh đồi núi:

### 1. Biểu Đồ Màu Sắc

**Mô tả:** Biểu đồ màu sắc nắm bắt sự phân bố màu sắc trong ảnh sử dụng không gian màu HSV (Hue-Saturation-Value: Màu sắc-Độ bão hòa-Độ sáng).

**Lý do lựa chọn:** 
- Đồi núi thường có mẫu màu đặc trưng - màu xanh da trời cho bầu trời, xanh lá cây/nâu cho thực vật, xám/trắng cho đá/tuyết
- Không gian màu HSV mang ý nghĩa cảm nhận hơn RGB đối với cảnh quan thiên nhiên
- Việc tách riêng các kênh màu sắc, độ bão hòa và độ sáng cho phép mô tả tốt hơn về cảnh quan đồi núi

**Giá trị thông tin:**
- Kênh màu sắc (hue) giúp xác định thời điểm trong ngày (màu hoàng hôn so với màu xanh giữa trưa)
- Độ bão hòa (saturation) nắm bắt độ rực rỡ của cảnh quan
- Độ sáng (value) giúp phân biệt giữa các khu vực bầu trời sáng và các sườn núi tối hơn

### 2. Đặc Trưng Cạnh

**Mô tả:** Đặc trưng cạnh phát hiện và phân tích các cạnh trong ảnh, tập trung vào mật độ và hướng của chúng.

**Lý do lựa chọn:**
- Đồi núi có mẫu cạnh đặc trưng với các hướng ngang và chéo mạnh mẽ
- Đặc trưng cạnh nắm bắt đường viền và hình dạng của các dãy núi
- Mật độ cạnh có thể giúp phân biệt giữa núi gồ ghề và núi trơn láng

**Giá trị thông tin:**
- Biểu đồ hướng cạnh nắm bắt các góc chủ đạo trong đường viền đồi núi
- Mật độ cạnh phân biệt giữa hình dạng núi đơn giản và phức tạp
- Các đặc trưng này bền vững đối với sự thay đổi ánh sáng

### 3. Đặc Trưng Kết Cấu (HOG)

**Mô tả:** Biểu đồ độ dốc hướng (Histogram of Oriented Gradients - HOG) nắm bắt các mẫu kết cấu và cấu trúc độ dốc cục bộ.

**Lý do lựa chọn:**
- Đồi núi có các mẫu kết cấu khác nhau giữa các bề mặt đá, khu vực phủ tuyết và sườn dốc có thực vật
- Đặc trưng HOG phù hợp để nắm bắt các khác biệt về kết cấu này
- Kết cấu là đặc trưng phân biệt chính giữa các loại núi khác nhau

**Giá trị thông tin:**
- Đặc trưng HOG nắm bắt cả hình dạng vĩ mô và kết cấu vi mô
- Chúng giúp phân biệt giữa núi phủ tuyết trơn láng và đỉnh núi đá gồ ghề
- Các đặc trưng này cung cấp thông tin không gian mà biểu đồ màu sắc đơn thuần không thể nắm bắt

### 4. Đặc Trưng Đường Chân Trời

**Mô tả:** Đặc trưng đường chân trời trích xuất thông tin về đường viền núi nổi bật trên nền trời.

**Lý do lựa chọn:**
- Đường chân trời/đường viền là một trong những đặc trưng nổi bật nhất của đồi núi
- Con người thường nhận ra núi bằng các đặc điểm hình dạng đặc trưng
- Sự biến đổi về chiều cao và độ gồ ghề của đường chân trời có thể là đặc trưng phân biệt mạnh mẽ

**Giá trị thông tin:**
- Độ gồ ghề của đường chân trời nắm bắt độ nhấp nhô của các đỉnh núi
- Chiều cao trung bình của đường chân trời cho biết núi chiếm phần lớn khung hình hay ở xa
- Các điểm đường chân trời được lấy mẫu tạo ra "chữ ký" đơn giản hóa của hình dạng núi

### 5. Entropy Ảnh

**Mô tả:** Entropy Shannon đo lường độ phức tạp tổng thể và lượng thông tin của ảnh.

**Lý do lựa chọn:**
- Đồi núi thay đổi về độ phức tạp trực quan - từ đơn giản với một đỉnh đến các dãy núi phức tạp
- Entropy cung cấp một giá trị duy nhất nắm bắt độ phức tạp tổng thể này
- Giúp phân biệt giữa các cảnh núi đơn giản và phức tạp về mặt trực quan

**Giá trị thông tin:**
- Entropy cao hơn gợi ý một cảnh núi phức tạp, chi tiết hơn
- Entropy thấp hơn có thể chỉ ra cảnh quan núi đơn giản, tối giản hơn
- Đóng vai trò như một đặc trưng toàn cục hữu ích để bổ sung cho các đặc trưng cục bộ hơn

## Khoảng Cách Euclidean Như Độ Đo Tương Đồng

Chúng tôi sử dụng khoảng cách Euclidean để đo lường độ tương đồng giữa các vector đặc trưng:

$$d(p,q) = \sqrt{\sum_{i=1}^{n} (p_i - q_i)^2}$$

Trong đó:
- p và q là các vector đặc trưng của hai ảnh
- n là số lượng đặc trưng
- p_i và q_i là các giá trị đặc trưng riêng lẻ

**Lý do lựa chọn khoảng cách Euclidean:**
1. **Diễn giải trực quan**: Giá trị khoảng cách nhỏ hơn chỉ ra sự tương đồng lớn hơn
2. **Hiệu quả tính toán**: Nhanh chóng để tính toán ngay cả với vector đặc trưng lớn
3. **Trọng số bằng nhau**: Mỗi chiều đặc trưng đóng góp như nhau vào thước đo tương đồng
4. **Được thiết lập tốt**: Được sử dụng rộng rãi trong các hệ thống truy xuất ảnh

## Cấu Trúc Vector Đặc Trưng

Vector đặc trưng cuối cùng cho mỗi ảnh đồi núi bao gồm:
- 96 đặc trưng biểu đồ màu (32 bins × 3 kênh)
- 19 đặc trưng cạnh (1 mật độ cạnh + 18 bin hướng)
- ~324 đặc trưng HOG (thay đổi theo kích thước ảnh)
- ~22 đặc trưng đường chân trời (20 điểm lấy mẫu + độ gồ ghề + chỉ số chiều cao)
- 1 đặc trưng entropy

Bộ đặc trưng toàn diện này nắm bắt cả đặc điểm toàn cục và cục bộ của ảnh đồi núi, cho phép so sánh tương đồng chính xác.

## Ưu Điểm Của Bộ Đặc Trưng Của Chúng Tôi

1. **Biểu diễn đa khía cạnh**: Kết hợp các thông số về màu sắc, hình dạng, kết cấu và độ phức tạp
2. **Độ bền vững**: Ít nhạy cảm với thay đổi ánh sáng hơn so với so sánh pixel thô
3. **Tính liên quan ngữ nghĩa**: Các đặc trưng tương ứng với các thuộc tính có ý nghĩa của đồi núi
4. **Biểu diễn nhỏ gọn**: Giảm dữ liệu ảnh đa chiều thành vector đặc trưng dễ quản lý
5. **Hiệu quả**: Các đặc trưng có thể được tính toán trước và lưu trữ để tìm kiếm tương đồng nhanh chóng 