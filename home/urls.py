# file định tuyến, xác định URL nào sẽ được xử lý bởi view nào

from django.urls import path, include #hàm từ module django.urls, ánh xạ URL
from . import views #tạo đối tượng view
from django.contrib.auth.views import LogoutView, LoginView #view Django để đăng nhập, xuất
from django.urls import reverse_lazy #hàm Django để lấy URL của view dựa trên name view
from map import views as map_views

# list URL app home (index, contact, register, login, logout)
urlpatterns = [
    path("", views.index, name='index'),# Đặt tên để tham chiếu URL bằng {% url 'index' %}
    path("contact/", views.contact, name='contact'),
    path("statistic/", views.statistic, name='statistic'),
    path("register/", views.register, name='register'),
    #LoginView.as_view() view class mặc định xử lý login, gồm các logic cần thiết, giảm việc tự viết code
    path('login/', LoginView.as_view(template_name='pages/login.html', success_url=reverse_lazy('index')), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('incidents/<int:incident_id>/', views.incident_detail, name='incident_detail'),
    path('incidents/<str:incident_type>/', views.incidents_list, name='incidents_list'),
    path('incidents/<str:incident_type>/<str:status>/', views.incidents_list, name='incidents_status_list'),
    path("map_statistic/", map_views.map_statistic, name='map_statistic'),
    path("maps/proxy/", map_views.google_maps_proxy, name="google_maps_proxy"),
    path('approve_incident/', views.approve_incident, name='approve_incident'),

]
