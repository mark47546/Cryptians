from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import CreatePostForm, UpdatePostForm, CreateCommentForm, UpdateCommentForm
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def homepage(request):
    return render(request,'home.html')


def allPost(request):
    search = request.GET.get('search')
    if search:
        data = Post.objects.filter(Q(title__icontains=search) & Q(title__icontains=search))
    else:
        data = Post.objects.all()
    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'post/all_post.html',{'post':page_obj})

def createPost(request):
    posted_by = request.user
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/allPost")
    else:
        form = CreatePostForm(initial={'posted_by':posted_by})
        return render(request,'Post/create_post.html', {'form':form})

def viewPost(request,post_id):
    get_post_id = Post.objects.get(id=post_id)
    return render(request, 'post/view_post.html',{'post':get_post_id})