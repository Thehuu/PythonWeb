#Tạo bảng trong CSDL lưu trữ thông tin về các điểm cứu trợ
#db trong Django liên quan đến thao tác CSDL
#models định nghĩa các cấu trúc dữ liệu, các thuộc tính (fields), mối quan hệ
from django.db import models
class ReliefLocation(models.Model):
    #CharField: Dùng cho chuỗi ngắn, bắt buộc phải cung cấp max_length
    #TextField: Dùng cho chuỗi dài, không yêu cầu max_length.
    name = models.CharField(max_length=255)  # Tên vị trí cứu trợ
    mobile=models.IntegerField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=13, decimal_places=6)  # Vĩ độ, lưu trữ tối đa 9 chữ số với 6 số sau dấu ,
    longitude = models.DecimalField(max_digits=13, decimal_places=6)  # Kinh độ
    description = models.TextField(blank=True)  # Mô tả thêm về vị trí
    created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rescued', 'Rescued'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Trạng thái cứu trợ

    #phương thức __str__(self) trả về giá trị của thuộc tính name
    #VD location = ReliefLocation(name="Central Park")
    #khi in hoặc hiển thị một đối tượng của ReliefLocation
    #thay vì hiển thị một chuỗi khó hiểu <ReliefLocation object (1)>
    #nó sẽ hiển thị tên của địa điểm cứu trợ.
    #location = ReliefLocation(name="Central Park")
    #print(location)
    #KQ Central Park
    #để thuận tiện sử dung trong django

    def __str__(self):
        return self.name
