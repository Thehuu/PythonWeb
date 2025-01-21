from django.http import JsonResponse
from django.shortcuts import render
from .models import ReliefLocation, Incident
from .forms import ReliefPointForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Hàm hiển thị bản đồ với các thông tin liên quan
def show_map(request):
    form = ReliefPointForm()  # Khởi tạo form để nhập thông tin điểm cứu trợ

    # Lọc các địa điểm cứu trợ đã được phê duyệt
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
    tngt_count = Incident.objects.filter(incident_type='TNGT').count()  # Tai nạn giao thông
    drowning_count = Incident.objects.filter(incident_type='DROWNING').count()  # Đuối nước
    fire_count = Incident.objects.filter(incident_type='FIRE').count()  # Cháy
    disaster_count = Incident.objects.filter(incident_type='DISASTER').count()  # Thiên tai

    # Tạo ngữ cảnh để truyền vào template
    context = {
        'form': form,  # Form để nhập dữ liệu
        'locations': locations_data,  # Danh sách các địa điểm cứu trợ
        'tngt_count': tngt_count,  # Tổng số tai nạn giao thông
        'drowning_count': drowning_count,  # Tổng số đuối nước
        'fire_count': fire_count,  # Tổng số vụ cháy
        'disaster_count': disaster_count,  # Tổng số thiên tai
    }

    # Kết xuất template và trả về phản hồi
    return render(request, 'map/map.html', context)

# Hàm lưu địa điểm cứu trợ vào cơ sở dữ liệu
def save_location(request):
    if request.method == 'POST':  # Kiểm tra nếu phương thức là POST
        form = ReliefPointForm(request.POST, request.FILES)  # Lấy dữ liệu từ request và khởi tạo form
        if form.is_valid():  # Kiểm tra tính hợp lệ của form
            form.save()  # Lưu dữ liệu vào cơ sở dữ liệu
            # Gửi thông báo
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications", # tên nhóm nhận thông báo
                {
                    "type": "send_notification",
                    "message": "Có khai báo mới!"
                }
            )
            # Chuyển hướng đến trang thành công
            return render(request, 'map/success.html')
        else:
            # Chuyển hướng đến trang lỗi với thông tin lỗi từ form
            return render(request, 'map/error.html', {'errors': form.errors})
    # Trả về phản hồi cho yêu cầu không hợp lệ
    return render(request, 'map/error.html', {'errors': 'Invalid request'})




# Hàm hiển thị bản đồ với các điểm cứu trợ
def map_statistic(request):
    form = ReliefPointForm()  # Khởi tạo form để nhập thông tin điểm cứu trợ

    # Lọc các địa điểm cứu trợ đã được phê duyệt
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
    tngt_count = Incident.objects.filter(incident_type='TNGT').count()  # Tai nạn giao thông
    drowning_count = Incident.objects.filter(incident_type='DROWNING').count()  # Đuối nước
    fire_count = Incident.objects.filter(incident_type='FIRE').count()  # Cháy
    disaster_count = Incident.objects.filter(incident_type='DISASTER').count()  # Thiên tai

    # Tạo ngữ cảnh để truyền vào template
    context = {
        'form': form,  # Form để nhập dữ liệu
        'locations': locations_data,  # Danh sách các địa điểm cứu trợ
        'tngt_count': tngt_count,  # Tổng số tai nạn giao thông
        'drowning_count': drowning_count,  # Tổng số đuối nước
        'fire_count': fire_count,  # Tổng số vụ cháy
        'disaster_count': disaster_count,  # Tổng số thiên tai
    }

    # Kết xuất template và trả về phản hồi
    return render(request, 'map/map_statistic.html', context)