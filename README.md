CÁC BƯỚC IMPORT CƠ SỞ DỮ LIỆU (Dùng file belu trong folder db)

Lưu ý: Phải sử dụng docker tạo container dùng mysql. Chi tiết hỏi trợ thủ đắc lực

Bước 1: Chạy lệnh import

docker exec -i mysql-container mysql -u root -p belu < belu.sql

Bước 2: Nhập mật khẩu được thiết lập sẵn là "matkhau"

Bước 3: Select thử xem 
