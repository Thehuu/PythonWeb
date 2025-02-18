#xử lý các yêu cầu HTTP từ trình duyệt và trả về phản hồi (response) tương ứng

from django.shortcuts import render
from .forms import RegistrationForm # .forms = file forms.py cùng thư mục
from django.http import HttpResponseRedirect
from map.models import ReliefLocation
from django.core.paginator import Paginator
from map.models import ReliefLocation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# def trang chủ
def index(request):
    # Lấy số lượng điểm với trạng thái 'pending' và 'rescued'
    pending_points_count = ReliefLocation.objects.filter(status='pending').count()
    approved_points_count = ReliefLocation.objects.filter(status='approved').count()
    # Render template
    return render(request, 'pages/home.html', {
        'pending_points_count': pending_points_count,
        'approved_points_count': approved_points_count,
    })

# def contact
def contact(request):
    return render(request,'pages/contact.html')

#def error_404
def error_404(request, exception):
    return render(request, 'home/404.html', status=404)

#def path error_500
def error_500(request):
    return render(request, 'pages/error.html')

#def register
def register(request):
    form = RegistrationForm() #tạo 1 form trống
    if request.method == 'POST': #kiểm tra có POST? POST khi nhấn nút "submit"
        form = RegistrationForm(request.POST) #request.POST chứa dữ liệu người dùng nhập vào form 
        if form.is_valid():
            form.save() #hàm save() tạo một đối tượng mới dựa trên dữ liệu nhập vào
            return HttpResponseRedirect ('/') #sao lưu xong thì chuyển hướng đến trang chủ
    return render(request,'pages/register.html',{'form':form}) #{'form':...} chuyển form sang HTML



def incidents_list(request, incident_type, status=None):
    if status:
        incidents = ReliefLocation.objects.filter(incident_type=incident_type, status=status).order_by('-created_at')
    else:
        incidents = ReliefLocation.objects.filter(incident_type=incident_type).order_by('-created_at')

    paginator = Paginator(incidents, 2)  # Mỗi trang hiển thị 2 vụ
    page_number = request.GET.get('page', 1)  # Lấy số trang từ query string
    page_obj = paginator.get_page(page_number)  # Lấy đối tượng trang hiện tại
    # Tính số thứ tự bắt đầu cho trang hiện tại
    start_index = (page_obj.number - 1) * paginator.per_page

    # Tính toán các trang cần hiển thị
    max_pages_to_show = 5
    current_page = page_obj.number
    total_pages = paginator.num_pages

    if total_pages <= max_pages_to_show:
        page_range = range(1, total_pages + 1)
    else:
        start_page = max(current_page - 2, 1)
        end_page = min(current_page + 2, total_pages)
        if start_page == 1:
            end_page = max_pages_to_show
        if end_page == total_pages:
            start_page = total_pages - max_pages_to_show + 1
        page_range = range(start_page, end_page + 1)

    return render(request, 'pages/incidents_list.html', {
        'incidents': page_obj,  # Đối tượng trang
        'start_index': start_index,  # Số thứ tự bắt đầu
        'status': status,
        'incident_type': incident_type,
        'page_obj': page_obj,
        'page_range': page_range,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
    })

from django.shortcuts import render, get_object_or_404
from map.models import ReliefLocation

def incident_detail(request, incident_id):
    # Lấy đối tượng ReliefLocation từ cơ sở dữ liệu dựa trên incident_id
    incident = get_object_or_404(ReliefLocation, id=incident_id)
    context = {
        'incident': incident,
        'user': request.user,  # Thêm đối tượng user vào context
    }
    return render(request, 'pages/incident_detail.html', context)

def statistic(request):
    # Render dữ liệu từ database vào vào statistic.html
    traffic_accidents_count = ReliefLocation.objects.filter(incident_type='traffic_accident').count()                        
    traffic_accidents_pending = ReliefLocation.objects.filter(incident_type='traffic_accident', status='pending').count()
    traffic_accidents_approved = ReliefLocation.objects.filter(incident_type='traffic_accident', status='approved').count()
    traffic_accidents_rescued = ReliefLocation.objects.filter(incident_type='traffic_accident', status='rescued').count()

    drowning_incidents_count = ReliefLocation.objects.filter(incident_type='drowning').count()
    drowning_incidents_pending = ReliefLocation.objects.filter(incident_type='drowning', status='pending').count()
    drowning_incidents_approved = ReliefLocation.objects.filter(incident_type='drowning', status='approved').count()
    drowning_incidents_rescued = ReliefLocation.objects.filter(incident_type='drowning', status='rescued').count()

    fire_incidents_count = ReliefLocation.objects.filter(incident_type='fire').count()
    fire_incidents_pending = ReliefLocation.objects.filter(incident_type='fire', status='pending').count()
    fire_incidents_approved = ReliefLocation.objects.filter(incident_type='fire', status='approved').count()
    fire_incidents_rescued = ReliefLocation.objects.filter(incident_type='fire', status='rescued').count()

    natural_disasters_count = ReliefLocation.objects.filter(incident_type='natural_disaster').count()
    natural_disasters_pending = ReliefLocation.objects.filter(incident_type='natural_disaster', status='pending').count()
    natural_disasters_approved = ReliefLocation.objects.filter(incident_type='natural_disaster', status='approved').count()
    natural_disasters_rescued = ReliefLocation.objects.filter(incident_type='natural_disaster', status='rescued').count()

    # Lấy danh sách sự kiện, sắp xếp theo thời gian giảm dần
    incidents = ReliefLocation.objects.order_by('-created_at')

    context = {
        'traffic_accidents_count': traffic_accidents_count,
        'traffic_accidents_pending': traffic_accidents_pending,
        'traffic_accidents_approved': traffic_accidents_approved,
        'traffic_accidents_rescued': traffic_accidents_rescued,
        'drowning_incidents_count': drowning_incidents_count,
        'drowning_incidents_pending': drowning_incidents_pending,
        'drowning_incidents_approved': drowning_incidents_approved,
        'drowning_incidents_rescued': drowning_incidents_rescued,
        'fire_incidents_count': fire_incidents_count,
        'fire_incidents_pending': fire_incidents_pending,
        'fire_incidents_approved': fire_incidents_approved,
        'fire_incidents_rescued': fire_incidents_rescued,
        'natural_disasters_count': natural_disasters_count,
        'natural_disasters_pending': natural_disasters_pending,
        'natural_disasters_approved': natural_disasters_approved,
        'natural_disasters_rescued': natural_disasters_rescued,
    }
    return render(request,'pages/statistic.html',context)

@csrf_exempt
def approve_incident(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        incident_id = data.get('incident_id')
        try:
            incident = ReliefLocation.objects.get(id=incident_id)
            incident.status = 'approved'
            incident.save()
            return JsonResponse({'success': True})
        except ReliefLocation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Incident not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

