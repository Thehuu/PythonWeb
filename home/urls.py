# file định tuyến, xác định URL nào sẽ được xử lý bởi view nào

from django.urls import path, include #hàm từ module django.urls, ánh xạ URL
from . import views #tạo đối tượng view
from django.contrib.auth.views import LogoutView, LoginView #view Django để đăng nhập, xuất
from django.urls import reverse_lazy #hàm Django để lấy URL của view dựa trên name view

# list URL app home (index, contact, register, login, logout)
urlpatterns = [
    path("", views.index, name='index'),# Đặt tên để tham chiếu URL bằng {% url 'index' %}
    path("contact/", views.contact, name='contact'),
    path("register/", views.register, name='register'),
    #LoginView.as_view() view class mặc định xử lý login, gồm các logic cần thiết, giảm việc tự viết code
    path('login/', LoginView.as_view(template_name='pages/login.html', success_url=reverse_lazy('index')), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('traffic-accidents/', views.traffic_accidents_list, name='traffic_accidents_list'),
    path('traffic-accidents/<str:status>/', views.traffic_accidents_list, name='traffic_accidents_status_list'),
    path('drowning-incidents/', views.drowning_incidents_list, name='drowning_incidents_list'),
    path('drowning-incidents/<str:status>/', views.drowning_incidents_list, name='drowning_incidents_status_list'),
    path('fire-incidents/', views.fire_incidents_list, name='fire_incidents_list'),
    path('fire-incidents/<str:status>/', views.fire_incidents_list, name='fire_incidents_status_list'),
    path('natural-disasters/', views.natural_disasters_list, name='natural_disasters_list'),
    path('natural-disasters/<str:status>/', views.natural_disasters_list, name='natural_disasters_status_list'),
]
