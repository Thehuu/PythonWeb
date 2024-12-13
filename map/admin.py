
from django.contrib import admin
from .models import ReliefLocation
#class để tùy chỉnh cách hiển thị của model ReliefLocation trong trang admin
class ReliefLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description')

#Đăng ký model ReliefLocation với trang quản trị
admin.site.register(ReliefLocation, ReliefLocationAdmin)
