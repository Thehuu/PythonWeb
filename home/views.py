#xử lý các yêu cầu HTTP từ trình duyệt và trả về phản hồi (response) tương ứng

from django.shortcuts import render
from .forms import RegistrationForm # .forms = file forms.py cùng thư mục
from django.http import HttpResponseRedirect

# def trang chủ
def index(request):
    #render() hàm tiện ích của Django. Lấy yêu cầu (request), tìm tệp home.html trả về trang html
    return render(request,'pages/home.html')

# def contact
def contact(request):
    return render(request,'pages/contact.html')

#def error_404
def error_404(request, exception):
    return render(request, 'pages/error.html')

#def path error_500
def error_500(request):
    return render(request, 'pages/error.html')

#def register
def register(request):
    form =RegistrationForm() #tạo 1 form trống
    if request.method=='POST': #kiểm tra có POST? POST khi nhấn nút "submit"
            form =RegistrationForm(request.POST) #request.POST chứa dữ liệu người dùng nhập vào form 
            if form.is_valid():
                 form.save() #hàm save() tạo một đối tượng mới dựa trên dữ liệu nhập vào
                 return HttpResponseRedirect ('/') #sao lưu xong thì chuyển hướng đến trang chủ
    else:
        return render(request,'pages/register.html',{'form':form}) #{'form':...} chuyển form sang HTML
