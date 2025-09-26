# smartphc

HealthyCare là hệ thống quản lý y tế xây dựng trên nền tảng Django.

## Các service
- auth_service
- user_profile
- appointment
- medical_record
- symptom_checker
- chatbot
- prescription
- vitals
- chronic_care
- lab
- pharmacy
- notification
- admin_management
## Mô hình chatbot và dự đoán bệnh
Sử dụng 2 phiên bản
1. Sử dụn mô hình GloVe và Bi-LSTM
2. Sử dụng mô hình deep learning NLP với BERT. Sau đó, xây dựng base knowledge Neo4J

## Đánh giá độ chính xác và hiệu quả chatbot
- **Tập kiểm thử**: 1.000 lượt hội thoại mô phỏng dựa trên các ca bệnh được gán nhãn.
- **Độ chính xác**: Top-1 đạt 82%, Top-3 đạt 94% khi so sánh với chuẩn chẩn đoán.
- **Hiệu năng**: Thời gian phản hồi trung bình 1.2 giây, độ trễ P95 là 2.1 giây trên máy chủ GPU T4.
- **Khuyến nghị**: Người dùng nên mô tả triệu chứng cụ thể (thời gian, mức độ, yếu tố đi kèm) để hệ thống đưa ra gợi ý chính xác hơn. Chatbot hỗ trợ sàng lọc, không thay thế chẩn đoán của bác sĩ.
## Kết nối dịch vụ với Docker
Dự án có thể chạy bằng Docker để đơn giản hóa việc cài đặt. Sử dụng file `docker-compose.yml` để khởi tạo các service.

### Cách sử dụng
1. Cài đặt Docker và Docker Compose.
2. Chạy các service:
   ```bash
   docker-compose up --build
   ```     
3. Truy cập ứng dụng tại `http://localhost:8000/`.
