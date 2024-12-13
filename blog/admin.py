#File admin.py trong ứng dụng blog được sử dụng để tùy chỉnh giao diện quản trị
from django.contrib import admin

from .models import Post

#class cho phép tùy chỉnh cách mà model Post được hiển thị và quản lý trong trang admin
class PostAdmin(admin.ModelAdmin):
    list_display=['title','date','body']
    list_filter=['title','date']
    search_fields=['title','body','id']
admin.site.register(Post, PostAdmin)