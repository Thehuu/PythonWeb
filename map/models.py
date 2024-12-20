#Tạo bảng trong CSDL lưu trữ thông tin về các điểm cứu trợ
#db trong Django liên quan đến thao tác CSDL
#models định nghĩa các cấu trúc dữ liệu, các thuộc tính (fields), mối quan hệ
from django.db import models

class ReliefLocation(models.Model):
    INCIDENT_CHOICES = [
        ('traffic_accident', 'Tai nạn giao thông'),
        ('drowning', 'Đuối nước'),
        ('fire', 'Cháy'),
        ('natural_disaster', 'Thiên tai'),
    ]

    incident_type = models.CharField(max_length=20, choices=INCIDENT_CHOICES,null=True)
    name = models.CharField(max_length=100)  # Tên vị trí cứu trợ
    mobile = models.CharField(max_length=15, null=True, blank=True)  # Số điện thoại liên hệ
    latitude = models.FloatField()  # Vĩ độ, lưu trữ tối đa 9 chữ số với 6 số sau dấu ,
    longitude = models.FloatField()  # Kinh độ
    description = models.TextField(blank=True, null=True)  # Mô tả thêm về vị trí cứu trợ
    image = models.ImageField(upload_to='images/', null=True, blank=True)
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





#có vẻ thừa chỗ này
class Incident(models.Model):
    TYPE_CHOICES = [
        ('TNGT', 'Tai nạn giao thông'),
        ('DROWNING', 'Đuối nước'),
        ('FIRE', 'Cháy'),
        ('DISASTER', 'Thiên tai'),
    ]
    incident_type = models.CharField(max_length=10, choices=TYPE_CHOICES)  # Loại sự kiện
    description = models.TextField()  # Mô tả sự kiện
    date = models.DateTimeField(auto_now_add=True)  # Thời gian xảy ra sự kiện

    def __str__(self):
        return f"{self.get_incident_type_display()} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
