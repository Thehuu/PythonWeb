#Định nghĩa model tên Post, đại diện cho một table trong CSDL
#Mỗi trường (field) của model tương ứng với colum in table

from django.db import models
from ckeditor.fields import RichTextField

#class Post sử dụng để tạo ra một table trong CSDL cho các bài viết (posts)
class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)
    body = RichTextField()

    def __str__(self):
        return self.title