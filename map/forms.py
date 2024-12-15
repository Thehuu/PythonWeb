# tạo form cho người dùng nhập thông tin từ giao diện

from django import forms
from .models import ReliefLocation

#tạo một ModelForm để người dùng có thể nhập thông tin và lưu vào cơ sở dữ liệu
#ModelForm là một lớp con của forms nhằm tạo ra các form
class ReliefPointForm(forms.ModelForm):
    INCIDENT_CHOICES = [
        ('traffic_accident', 'Tai nạn giao thông'),
        ('drowning', 'Đuối nước'),
        ('fire', 'Cháy'),
        ('natural_disaster', 'Thiên tai'),
    ]

    incident_type = forms.ChoiceField(choices=INCIDENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), label='Lựa chọn khai báo')

#class logic xử lý: Nếu muốn thêm các phương thức clean(), save().
    class Meta:
    #định nghĩa các thông tin cấu hình quan trọng cho form
    #Meta thể hiện rằng lớp này quản lý "metadata" của form
        model = ReliefLocation # Chỉ định form sẽ tuân theo model ReliefLocation
        fields = ['incident_type', 'name', 'mobile', 'description', 'image']# Chỉ định các trường hiển thị trong form: 'latitude', 'longitude',
        labels = {
            'name': 'Họ và tên',  # Đổi nhãn cho trường name
            'mobile':'Số điện thoại',
            #'latitude': 'Vĩ độ (click vào điểm trên map)', # Chỉ dẫn cho người dùng về cách nhập vĩ độ
            #'longitude': 'Kinh độ (click vào điểm trên map)', # Chỉ dẫn cho người dùng về cách nhập kinh độ
            'description': 'Mô tả thêm',
            'image': 'Hình ảnh',
        }
                
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}), # Thiết lập widget cho trường tên người dùng
            'mobile': forms.TextInput(attrs={'class': 'form-control'}), # Thiết lập widget cho trường số điện thoại
           # 'latitude': forms.NumberInput(attrs={'class': 'form-control'}), # Thiết lập widget cho trường vĩ độ
            #'longitude': forms.NumberInput(attrs={'class': 'form-control'}), # Thiết lập widget cho trường kinh độ
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), # Thiết lập widget cho trường mô tả
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}), # Thiết lập widget cho trường hình ảnh
        }
