
# ánh xạ các URL được người dùng truy cập đến các view tương ứng trong views.py
from django.urls import path
from . import views

#url list blog, detail blog/1, blog/2 = {% url 'post' id=1 %}
urlpatterns = [
    path('', views.PostListView.as_view(),name='blog'),# hiển thị danh sách các bài viết
    path('<int:id>/',views.post,name='post'),# hiển thị chi tiết bài. file html có thể dùng {% url 'post' id=1 %}

]