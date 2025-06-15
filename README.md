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

## Kết nối dịch vụ với Docker
Dự án có thể chạy bằng Docker để đơn giản hóa việc cài đặt. Sử dụng file `docker-compose.yml` để khởi tạo các service.

### Cách sử dụng
1. Cài đặt Docker và Docker Compose.
2. Chạy các service:
   ```bash
   docker-compose up --build
   ```
3. Truy cập ứng dụng tại `http://localhost:8000/`.
