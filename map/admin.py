from django.contrib import admin
from django.utils.html import format_html
from .models import ReliefLocation

# Class để tùy chỉnh cách hiển thị của model ReliefLocation trong trang admin
class ReliefLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'incident_type', 'formatted_created_at','formatted_address','status','google_map_link')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('google_map_link',)  # Thêm google_map_link vào readonly_fields

    exclude = ('latitude', 'longitude')  # Ẩn các trường latitude và longitude


    def google_map_link(self, obj):
        return format_html(
            '<a href="https://www.google.com/maps/search/?api=1&query={},{}" target="_blank">Google map</a>',
            obj.latitude,
            obj.longitude
        )
    google_map_link.short_description = 'Maps'

    # Hiển thị địa điểm dưới dạng HTML
    def formatted_address(self, obj):
        return format_html(
            # trong models.py để lấy địa chỉ từ tọa độ GPS
            obj.address,
            obj.latitude,
            obj.longitude,
        )
    formatted_address.short_description = 'Địa điểm GPS'


    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%H:%M %d/%m/%Y')
    formatted_created_at.short_description = 'Thời gian khai báo'

# Đăng ký model ReliefLocation với trang quản trị
admin.site.register(ReliefLocation, ReliefLocationAdmin)

