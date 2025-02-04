#Tạo bảng trong CSDL lưu trữ thông tin về các điểm cứu trợ
#db trong Django liên quan đến thao tác CSDL
#models định nghĩa các cấu trúc dữ liệu, các thuộc tính (fields), mối quan hệ
from django.db import models
from geopy.geocoders import Nominatim


class ReliefLocation(models.Model):
    INCIDENT_CHOICES = [
        ('traffic_accident', 'Tai nạn giao thông'),
        ('drowning', 'Đuối nước'),
        ('fire', 'Cháy'),
        ('natural_disaster', 'Thiên tai'),
    ]

    incident_type = models.CharField(max_length=20, choices=INCIDENT_CHOICES, verbose_name='Phân loại')
    name = models.CharField(max_length=100, verbose_name='Họ và tên')  # Tên người yêu cầu cứu trợ
    mobile = models.CharField(max_length=15, null=True, verbose_name='Điện thoại')  # Số điện thoại liên hệ
    residence = models.CharField(max_length=300, null=True, verbose_name='Nơi cư trú')  # Nơi cư trú
    latitude = models.FloatField(verbose_name='Vĩ độ')  # Vĩ độ, lưu trữ tối đa 9 chữ số với 6 số sau dấu ,
    longitude = models.FloatField(verbose_name='Kinh độ')  # Kinh độ
    address = models.CharField(max_length=300, null=True, verbose_name='Địa điểm GPS')  # Thêm trường address để lưu địa chỉ
    description = models.CharField(max_length=300, null=True,verbose_name='Ghi chú' )  # Mô tả thêm về vị trí cứu trợ
    image = models.ImageField(upload_to='images/', null=True, blank=True,verbose_name='Hình ảnh')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian khai báo')  # Thời gian tạo
    STATUS_CHOICES = [
        ('pending', 'Chờ duyệt'),
        ('approved', 'Duyệt'),
        ('rescued', 'Đã giải quyết'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Xử lý thông tin')  # Trạng thái cứu trợ

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Thông tin'

    def __str__(self):
        return self.name

    def formatted_created_at(self):
        return self.created_at.strftime('%H:%M %d/%m/%Y ')
    formatted_created_at.short_description = 'Thời gian khai báo'

    # Lấy địa chỉ từ tọa độ GPS
    def get_address_from_coordinates(self):
        geolocator = Nominatim(user_agent="myGeocoder", timeout=10)
        try:
            location = geolocator.reverse((self.latitude, self.longitude), language="vi")
            return location.address if location else "Không xác định"
        except GeocoderTimedOut:
            return "Không thể lấy địa chỉ (timeout)"
    # Ghi đè phương thức save của model để tự động lấy và lưu địa chỉ khi đối tượng được lưu.
    def save(self, *args, **kwargs):
        if not self.address:
            self.address = self.get_address_from_coordinates()
        super().save(*args, **kwargs)