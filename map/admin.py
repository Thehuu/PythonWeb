from django.contrib import admin
from .models import ReliefLocation, Incident

# Class để tùy chỉnh cách hiển thị của model ReliefLocation trong trang admin
class ReliefLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description')

# Đăng ký model ReliefLocation với trang quản trị
admin.site.register(ReliefLocation, ReliefLocationAdmin)

# Class để tùy chỉnh cách hiển thị của model Incident trong trang admin
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('incident_type', 'description', 'date')
    list_filter = ('incident_type', 'date')
    search_fields = ('description',)

# Đăng ký model Incident với trang quản trị
admin.site.register(Incident, IncidentAdmin)
