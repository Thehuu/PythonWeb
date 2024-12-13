
#xây dựng một hệ thống blog cơ bản với khả năng hiển thị danh sách bài viết và xem chi tiết bài viết
from django.shortcuts import render

# Create your views here.
from .models import Post
from django.views.generic import ListView

#class hiển thị danh sách bài viết
class PostListView(ListView):
    #queryset, template_name, context_object_name,paginate_by là thuộc tính của class PostListView
    queryset=Post.objects.all().order_by("-date") #truy vấn CSDL từ các đối tượng Post từ table CSDL
    template_name='blog/blog.html'#template HTML hiển thị danh sách bài viết
    context_object_name='Posts' #Posts tên biến trong blog.html
    paginate_by=10 # phân 10bài/trang

#def hiển thị chi tiết của một bài viết
def post(request,id):
    post = Post.objects.get(id=id)
    return render (request,'blog/post.html',{'post':post})