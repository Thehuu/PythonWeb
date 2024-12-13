"""
URL configuration for PythonWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include #kết nối các tệp urls.py
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings

#bổ sung các app home,blog
urlpatterns = [
    path('admin/', admin.site.urls),  # có sẵn
    path("", include("home.urls")),
    path("blog/",include("blog.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("map/",include("map.urls")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Nếu debug được bật, sẽ hiển thị trên trang WEB các lỗi cụ thể
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#xử lý các response 404, 500
handler404 = 'home.views.error_404'
handler500 = 'home.views.error_500'


