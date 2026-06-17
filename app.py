from pickledb import PickleDB

# 1. Khởi tạo hoặc tải cơ sở dữ liệu từ file 'test_db.json'
# Nếu file chưa tồn tại, pickleDB sẽ tự động tạo mới.
db = PickleDB("test_db.json").load()

# 2. Ghi dữ liệu vào (Khóa - Giá trị)
db.set("ten_du_an", "pickleDB v1.6")
db.set("phien_ban", 1.6)
db.set("danh_sach_tinh_nang", ["Sử dụng orjson", "Hỗ trợ Async", "Hỗ trợ SQLite"])

print("--- Đã ghi dữ liệu thành công ---")

# 3. Đọc dữ liệu ra bằng Khóa (Key)
ten = db.get("ten_du_an")
phien_ban = db.get("phien_ban")
tinh_nang = db.get("danh_sach_tinh_nang")

print(f"Tên dự án: {ten}")
print(f"Phiên bản: {phien_ban}")
print(f"Tính năng nổi bật: {tinh_nang}")

# 4. Kiểm tra sự tồn tại của khóa (Dùng phương thức .get() kiểm tra khác None)
if db.get("ten_du_an") is not None:
    print("\nKhóa 'ten_du_an' có tồn tại trong DB.")