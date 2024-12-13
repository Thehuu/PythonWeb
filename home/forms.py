# tạo form đăng nhập

from django import forms
import re #biểu thức chính quy
from django.contrib.auth.models import User # Cung cấp trường và phương thức để tạo, quản lý user
from django.core.exceptions import ObjectDoesNotExist #kiểm tra xem đối tượng có tồn tại trong CSDL


# class định nghĩa form đăng ký người dùng trong Django kế thừa lớp forms.Form
class RegistrationForm(forms.Form): #form.Form là class cha
    username = forms.CharField(label="Tài khoản", max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput()) # PasswordInput làm đầu ẩn dưới dạng * hoặc ...
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())

    #def kiẻm tra, trả về pass hợp lệ
    def clean_password2(self):
        #self.cleaned_data là nơi lưu trữ các dữ liệu đã được "cleaned" (tức là các dữ liệu người dùng đã nhập vào form
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2 #Trả về mật khẩu được kiểm tra hợp lệ để Django lưu vào cleaned_data. 
        raise forms.ValidationError('Mật khẩu không hợp lệ')

    # def kiểm tra user có hợp lệ,user đã tồn tại
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username): #kiểm tra username chỉ chứa các ký tự a-Z, 0-9 và _
            raise forms.ValidationError('Không được có ký tự đặc biệt trong tên tài khoản')
        try:
            User.objects.get(username=username) #User model mặc định Django quản lý user 
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Tài khoản đã tồn tại')
    
    #def save một người dùng mới
    def save(self):
        User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )

