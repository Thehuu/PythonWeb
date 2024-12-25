# file định tuyến, xác định URL nào sẽ được xử lý bởi view nào

from django.urls import path, include #hàm từ module django.urls, ánh xạ URL
from . import views #tạo đối tượng view
# from django.contrib.auth.views import LogoutView, LoginView #view Django để đăng nhập, xuất
# from django.urls import reverse_lazy #hàm Django để lấy URL của view dựa trên name view

# list URL app home (index, contact, register, login, logout)
urlpatterns = [
    path("", views.index, name='index')]
