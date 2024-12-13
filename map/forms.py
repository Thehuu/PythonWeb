# tạo form cho người dùng nhập thông tin từ giao diện

from django import forms

from .models import ReliefLocation


#tạo một ModelForm để người dùng có thể nhập thông tin và lưu vào cơ sở dữ liệu
#ModelForm là một lớp con của forms nhằm tạo ra các form
class ReliefPointForm(forms.ModelForm):
#class logic xử lý: Nếu muốn thêm các phương thức clean(), save().
    class Meta:
    #định nghĩa các thông tin cấu hình quan trọng cho form
    #Meta thể hiện rằng lớp này quản lý "metadata" của form
        model = ReliefLocation # Chỉ định form sẽ tuân theo model ReliefLocation
        fields = ['name', 'mobile','latitude', 'longitude', 'description',]# Chỉ định các trường hiển thị trong form
        labels = {
            'name': 'Họ và tên',  # Đổi nhãn cho trường name
            'mobile':'Số điện thoại',
            'latitude': 'Vĩ độ (click vào điểm trên map)',
            'longitude': 'Kinh độ (click vào điểm trên map)',
            'description': 'Mô tả thêm',
        }
                
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }