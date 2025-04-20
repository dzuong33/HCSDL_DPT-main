import os
import shutil
import re

# Tạo thư mục mới không dấu
new_folder = 'mountain_images'
if not os.path.exists(new_folder):
    os.makedirs(new_folder)

# Thư mục gốc chứa ảnh
original_folder = 'ảnh xóa bg/ảnh xóa bg'

# Hàm để tạo tên file hợp lệ
def create_valid_filename(filename):
    # Loại bỏ phần mở rộng
    name, ext = os.path.splitext(filename)
    # Thay thế các ký tự không phải chữ cái, số bằng dấu gạch dưới
    valid_name = re.sub(r'[^\w\d]', '_', name)
    # Thêm lại phần mở rộng
    return f"{valid_name}{ext}"

# Đổi tên và sao chép các file ảnh
if os.path.exists(original_folder):
    files = os.listdir(original_folder)
    print(f"Tìm thấy {len(files)} file trong thư mục gốc")
    
    for i, filename in enumerate(files):
        # Tạo tên file mới
        new_filename = f"mountain_{i+1:03d}.jpg"
        
        # Đường dẫn đầy đủ
        original_path = os.path.join(original_folder, filename)
        new_path = os.path.join(new_folder, new_filename)
        
        # Sao chép file với tên mới
        try:
            shutil.copy2(original_path, new_path)
            print(f"Đã sao chép: {filename} -> {new_filename}")
        except Exception as e:
            print(f"Lỗi khi sao chép {filename}: {e}")
else:
    print(f"Không tìm thấy thư mục: {original_folder}")

print("Hoàn tất quá trình đổi tên và sao chép file")

# Cập nhật đường dẫn trong các file Python
files_to_update = ['mountain_image_analysis.py', 'mountain_attribute_demo.py']

for file in files_to_update:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Thay thế đường dẫn
        updated_content = content.replace("'Ảnh đồi núi/Ảnh đồi núi'", f"'{new_folder}'")
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Đã cập nhật đường dẫn trong file: {file}")
    else:
        print(f"Không tìm thấy file: {file}")

print("Quá trình hoàn tất. Bạn có thể chạy lại các script phân tích ảnh.") 