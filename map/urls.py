# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_map, name='show_map'),  # Hiển thị bản đồ và form
    path('save_location', views.save_location, name='save_location'),  # Lưu vị trí cứu trợ
]
