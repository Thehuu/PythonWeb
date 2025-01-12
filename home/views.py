#xử lý các yêu cầu HTTP từ trình duyệt và trả về phản hồi (response) tương ứng

from django.shortcuts import render
from .forms import RegistrationForm # .forms = file forms.py cùng thư mục
from django.http import HttpResponseRedirect
from map.models import ReliefLocation
from django.core.paginator import Paginator


# def trang chủ
def index(request):
    return render(request,'pages/home.html')

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


from django.core.paginator import Paginator

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

    return render(request, 'pages/incidents_list.html', {
        'incidents': page_obj,  # Đối tượng trang
        'start_index': start_index,  # Số thứ tự bắt đầu
        'status': status,
        'incident_type': incident_type
    })

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