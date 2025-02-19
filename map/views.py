from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse
import requests

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import ReliefLocation
from .forms import ReliefPointForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Hàm hiển thị bản đồ với các thông tin liên quan.API để ở đây vì url đang trỏ về show_map
def show_map(request):
    form = ReliefPointForm()  # Khởi tạo form để nhập thông tin điểm cứu trợ

    # Lọc các địa điểm cứu trợ đã được phê duyệt mới lên bản đồ
    locations = ReliefLocation.objects.filter(status='approved')

    # Chuyển đổi dữ liệu địa điểm thành danh sách các từ điển
    locations_data = [
        {
            'name': loc.name,  # Tên địa điểm
            'mobile': loc.mobile,  # Số điện thoại liên hệ
            'residence': loc.residence, #nơi cư trú
            'latitude': float(loc.latitude),  # Vĩ độ
            'longitude': float(loc.longitude),  # Kinh độ
            'description': loc.description,  # Mô tả địa điểm
            'incident_type': loc.incident_type,  # Loại sự cố

        }
        for loc in locations
    ]

    # Đếm số lượng sự cố theo từng loại
    tngt_count = ReliefLocation.objects.filter(incident_type='TNGT').count()  # Tai nạn giao thông
    drowning_count = ReliefLocation.objects.filter(incident_type='DROWNING').count()  # Đuối nước
    fire_count = ReliefLocation.objects.filter(incident_type='FIRE').count()  # Cháy
    disaster_count = ReliefLocation.objects.filter(incident_type='DISASTER').count()  # Thiên tai

    # Tạo ngữ cảnh để truyền vào template.Chỗ này cung cần API
    context = {
        'form': form,  # Form để nhập dữ liệu
        'locations': locations_data,  # Danh sách các địa điểm cứu trợ
        'tngt_count': tngt_count,  # Tổng số tai nạn giao thông
        'drowning_count': drowning_count,  # Tổng số đuối nước
        'fire_count': fire_count,  # Tổng số vụ cháy
        'disaster_count': disaster_count,  # Tổng số thiên tai
        "GOOGLE_MAPS_API_URL": f"https://maps.googleapis.com/maps/api/js?key={settings.GOOGLE_MAPS_API_KEY}&libraries=places"


    }

    # Kết xuất template và trả về phản hồi
    return render(request, 'map/map.html', context)

# Hàm lưu địa điểm cứu trợ vào cơ sở dữ liệu
def save_location(request):
    if request.method == 'POST':  # Kiểm tra nếu phương thức là POST
        form = ReliefPointForm(request.POST, request.FILES)  # Lấy dữ liệu từ request và khởi tạo form
        if form.is_valid():  # Kiểm tra tính hợp lệ của form
            location = form.save()  # Lưu dữ liệu vào cơ sở dữ liệu và lấy đối tượng đã lưu
            # Gửi thông báo khi có điểm cứu trợ mới
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications",  # tên nhóm nhận thông báo. Dữ liệu này sẽ được gửi đến consumers.NotificationConsumer
                {
                    "type": "send_notification",
                    "message": "Khai báo mới!",
                    "incident_id": location.id,  # Bao gồm incident_id trong thông báo
                }
            )
            # Chuyển hướng đến trang thành công

            return render(request, 'map/success.html')
        else:
            # Chuyển hướng đến trang lỗi với thông tin lỗi từ form
            return render(request, 'map/error.html', {'errors': form.errors})
    # Trả về phản hồi cho yêu cầu không hợp lệ
    return render(request, 'map/error.html', {'errors': 'Invalid request'})

# @permission_required('home.can_approve_incident')
@permission_required('map.can_approve_incident')
def approve_incident(request):
    if request.method == 'POST':
        incident_id = request.POST.get('incident_id')
        incident = get_object_or_404(ReliefLocation, id=incident_id)
        incident.status = 'approved'
        incident.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@permission_required('map.can_resolve_incident')
def resolve_incident(request, location_id):
    if request.method == 'POST':
        incident = get_object_or_404(ReliefLocation, id=location_id)
        incident.status = 'rescued'
        incident.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# Hàm hiển thị bản đồ với các điểm cứu trợ (lấy dữ liệu từ DB)
def map_statistic(request):
    form = ReliefPointForm()  # Khởi tạo form để nhập thông tin điểm cứu trợ

    # Lọc các địa điểm cứu trợ đã được phê duyệt
    locations = ReliefLocation.objects.filter(status='approved')

    # Chuyển đổi dữ liệu địa điểm thành danh sách các từ điển
    locations_data = [
        {
            'id': loc.id,
            'name': loc.name,  # Tên địa điểm
            'mobile': loc.mobile,  # Số điện thoại liên hệ
            'residence': loc.residence, #nơi cư trú
            'address': loc.address, #địa điểm gặp sự cố
            'latitude': float(loc.latitude),  # Vĩ độ
            'longitude': float(loc.longitude),  # Kinh độ
            'description': loc.description,  # Mô tả
            'incident_type': loc.incident_type,  # Loại sự cố
            'status': loc.status,  # Trạng thái
        }
        for loc in locations
    ]

    # Đếm số lượng sự cố theo từng loại
    tngt_count = ReliefLocation.objects.filter(incident_type='TNGT').count()  # Tai nạn giao thông
    drowning_count = ReliefLocation.objects.filter(incident_type='DROWNING').count()  # Đuối nước
    fire_count = ReliefLocation.objects.filter(incident_type='FIRE').count()  # Cháy
    disaster_count = ReliefLocation.objects.filter(incident_type='DISASTER').count()  # Thiên tai

    # Định nghĩa biến user_has_permission
    user_has_permission = request.user.has_perm('map.can_resolve_incident')

    # Tạo ngữ cảnh để truyền vào template
    context = {
        'form': form,  # Form để nhập dữ liệu
        'locations': locations_data,  # Danh sách các địa điểm cứu trợ
        'tngt_count': tngt_count,  # Tổng số tai nạn giao thông
        'drowning_count': drowning_count,  # Tổng số đuối nước
        'fire_count': fire_count,  # Tổng số vụ cháy
        'disaster_count': disaster_count,  # Tổng số thiên tai
        'userHasPermission': user_has_permission,  # Truyền biến userHasPermission vào ngữ cảnh
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    }

    # Kết xuất template và trả về phản hồi
    return render(request, 'map/map_statistic.html', context)


#  bạn tạo một API trên backend để gọi Google Maps và trả về script.
def google_maps_proxy(request):
    url = f"https://maps.googleapis.com/maps/api/js?key={settings.GOOGLE_MAPS_API_KEY}&libraries=places"
    response = requests.get(url)
    return HttpResponse(response.content, content_type=response.headers["Content-Type"])


