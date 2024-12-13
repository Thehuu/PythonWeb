#view functions điều khiển luồng xử lý dữ liệu giữa người dùng và DB 
from django.http import JsonResponse
from django.shortcuts import render
from .models import ReliefLocation
from .forms import ReliefPointForm

#render form cho người dùng nhập; render các điểm đã duyệt => map/map.html
def show_map(request):
    form = ReliefPointForm() #trả về form trống nhập dữ liệu
    locations = ReliefLocation.objects.filter(status='approved')# truy vấn DB trả về các điểm approved
    locations_data = [{'name': loc.name, 'mobile': loc.mobile ,'latitude': float(loc.latitude), 'longitude': float(loc.longitude), 'description': loc.description} for loc in locations]
    #sử dụng render sẽ truyền một từ điển (context) chứa các biến vào template map/map.html
    #các biến form và locations được truyền từ hàm show_map để hiển thị form nhập liệu và danh sách các điểm đã duyệt
    print(locations_data)  # In ra console để kiểm tra dữ liệu locations trước khi render
    return render(request, 'map/map.html', {'form': form, 'locations': locations_data})

#xử lý yêu cầu POST từ phía client,
def save_location(request):
    if request.method == 'POST':
        form = ReliefPointForm(request.POST)
        if form.is_valid():
            location = form.save()
            return JsonResponse({'status': 'Gui_thanh_cong', 'location_id': location.id})
        else:
            return JsonResponse({'status': 'failed', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'failed'}, status=400)

