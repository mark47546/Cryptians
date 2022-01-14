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


def myPost(request):
    #Query Data from model
    search_post = request.GET.get('search')
    if search_post:
        search_post = Post.objects.filter(Q(title__icontains=search_post) & Q(title__icontains=search_post))
        data = search_post.filter(posted_by=request.user)
    else:
        data = Post.objects.filter(posted_by=request.user)

    count = Post.objects.filter(posted_by=request.user)
    count_my_post = len(count)
    return render(request,'post/my_post.html',{'post':data, 'count_my_post':count_my_post})


def editPost(request,post_id):
    posted_by = request.user
    get_post_id = Post.objects.get(id=post_id)
    if posted_by == get_post_id.posted_by:
        form = CreatePostForm(instance=get_post_id)
    else: 
        pass
    return render(request,'post/edit_post.html',{'form':form,'post':get_post_id, 'posted_by':posted_by})

def updatePost(request,post_id):
    get_post_id = Post.objects.get(id=post_id)
    posted_by = request.user
    form = UpdatePostForm(request.POST,request.FILES, instance=get_post_id)
    if form.is_valid():
        form.save()
        return redirect("/myPost")
    else:
        return render(request,'post/edit_post.html',{'form':form,'post':get_post_id, 'posted_by':posted_by})

def deletePost(request,post_id):
    posted_by = request.user
    get_post_id = Post.objects.get(id=post_id)
    if posted_by == get_post_id.posted_by:
        get_post_id.delete()
    else:
        pass
    return redirect("/myPost")