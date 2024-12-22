# tạo form cho người dùng nhập thông tin từ giao diện

from django import forms
from .models import ReliefLocation

#tạo một ModelForm để người dùng có thể nhập thông tin và lưu vào cơ sở dữ liệu
#ModelForm là một lớp con của forms nhằm tạo ra các form
class ReliefPointForm(forms.ModelForm):
    class Meta:
        model = ReliefLocation
        fields = ['incident_type', 'name', 'mobile', 'latitude', 'longitude', 'description', 'image', 'residence']
        widgets = {
            'incident_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            #'latitude': forms.TextInput(attrs={'class': 'form-control'}),
            #'longitude': forms.TextInput(attrs={'class': 'form-control'}),
            'residence':forms.Textarea(attrs={'class': 'form-control','rows': 1}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows': 1}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'incident_type': 'Lựa chọn khai báo',
            'name': 'Họ tên',
            'mobile': 'Điện thoại',
            'residence': 'Nơi cư trú',
            'description' : "Ghi chú",
            'image': 'Hình ảnh',
        }
