from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import CreatePostForm, UpdatePostForm, CreateCommentForm, UpdateCommentForm
from django.core.paginator import Paginator
from django.db.models import Q
from taggit.models import Tag
from .forms import CreatePostForm
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.template.defaultfilters import slugify

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
    common_tags = Post.tags.most_common()[:4]

    return render(request,'post/all_post.html',{'post':page_obj,'common_tags':common_tags})

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Post.tags.most_common()[:4]
    data = Post.objects.filter(tags=tag)
    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post/all_post.html', {'post':page_obj,'common_tags':common_tags})

def createPost(request):
    posted_by = request.user
    common_tags = Post.tags.most_common()[:4]
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/allPost")
    else:
        form = CreatePostForm(initial={'posted_by':posted_by})
        return render(request,'Post/create_post.html', {'form':form, 'common_tags':common_tags})

def viewPost(request,post_id):
    posted_by = request.user
    get_post_id = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post = post_id)
    form = CreatePostForm(initial={'posted_by':posted_by})
    if request.method == "POST":
        form = CreateCommentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f"/allPost/{get_post_id.id}")
    
    return render(request, 'post/view_post.html',{'post':get_post_id, 'form':form, 'comments':comments})


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
    common_tags = Post.tags.most_common()[:4]
    if posted_by == get_post_id.posted_by:
        form = CreatePostForm(instance=get_post_id)
    else: 
        pass
    return render(request,'post/edit_post.html',{'form':form,'post':get_post_id, 'posted_by':posted_by, 'common_tags':common_tags})

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
    if posted_by == get_post_id.posted_by or posted_by.is_staff or posted_by.is_superuser:
        get_post_id.delete()
    else:
        pass
    return redirect("/myPost")

def deleteComment(request,comment_id,post_id):
    posted_by = request.user
    get_comment_id = Comment.objects.get(id=comment_id)
    if posted_by == get_comment_id.posted_by or posted_by.is_staff or posted_by.is_superuser:
        get_comment_id.delete()
    else:
        pass
    return redirect(f"/allPost/{get_comment_id.post.id}")