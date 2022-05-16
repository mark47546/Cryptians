from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Post, Comment, Tweet ,User
from .forms import CreatePostForm, UpdatePostForm, CreateCommentForm, UpdateCommentForm
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from .twitter import *
from taggit.models import Tag
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from predict.views import download_all

logger = logging.getLogger('__name__')
def update_twitter():
    print("-----------------------------Update twitter-----------------------------")
    save_to_db()

scheduler = BackgroundScheduler() 
scheduler.add_job(update_twitter, 'cron', minute='15')
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.core import serializers

@csrf_exempt
@api_view(["GET"])
def MyPostList(request):
    data = Post.objects.filter(posted_by=request.user)
    tmpJson = serializers.serialize("json",data)
    tmpObj = json.loads(tmpJson)
    return HttpResponse(json.dumps(tmpObj))


def homepage(request):
    first_login = str('first-login')
    num_visits = request.session.get(first_login, 1)
    request.session[first_login] = num_visits + 1
    if num_visits == 1:
        download_all()
        save_to_db()

    post = Post.objects.all().order_by('-id')[:4]
    common_tags = Post.tags.most_common()[:4].annotate(posts_count=Count('post'))
    context={'post':post,'common_tags':common_tags}
    return render(request,'home.html',context)

def realtime_graph(request):
    return render(request,'realtime_graph.html')



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
    tag = get_object_or_404(Tag, name=slug)
    common_tags = Post.tags.most_common()[:4]
    data = Post.objects.filter(tags=tag)
    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post/all_post.html', {'post':page_obj,'common_tags':common_tags})

@login_required
def createPost(request):
    posted_by = request.user
    common_tags = Post.tags.most_common()[:4]
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/allPost")
        logger.warning(f'Username {posted_by}: Got something went wrong when try to post')
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
        logger.warning(f'Username {posted_by}: Got something went wrong when try to comment')
    
    return render(request, 'post/view_post.html',{'post':get_post_id, 'form':form, 'comments':comments})

@login_required
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

@login_required
def editPost(request,post_id):
    posted_by = request.user
    get_post_id = Post.objects.get(id=post_id)
    common_tags = Post.tags.most_common()[:4]
    if posted_by == get_post_id.posted_by:
        form = CreatePostForm(instance=get_post_id)
    else: 
        pass
    return render(request,'post/edit_post.html',{'form':form,'post':get_post_id, 'posted_by':posted_by, 'common_tags':common_tags})

@login_required
def updatePost(request,post_id):
    get_post_id = Post.objects.get(id=post_id)
    posted_by = request.user
    form = UpdatePostForm(request.POST,request.FILES, instance=get_post_id)
    if form.is_valid():
        form.save()
        return redirect("/myPost")
    else:
        return render(request,'post/edit_post.html',{'form':form,'post':get_post_id, 'posted_by':posted_by})

@login_required
def deletePost(request,post_id):
    posted_by = request.user
    get_post_id = Post.objects.get(id=post_id)
    if posted_by == get_post_id.posted_by or posted_by.is_staff or posted_by.is_superuser:
        get_post_id.delete()
    else:
        pass
    return redirect("/myPost")

@login_required
def deleteComment(request,comment_id,post_id):
    posted_by = request.user
    get_comment_id = Comment.objects.get(id=comment_id)
    if posted_by == get_comment_id.posted_by or posted_by.is_staff or posted_by.is_superuser:
        get_comment_id.delete()
    else:
        pass
    return redirect(f"/allPost/{get_comment_id.post.id}")

@login_required
def tweet_list(request):

    search = request.GET.get('search')
    tweets = Tweet.objects.order_by('-published_date')
    if search:
        tweets = tweets.filter(Q(tweet_text__icontains=search) & Q(tweet_text__icontains=search))

    paginator = Paginator(tweets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'twitter/twitter.html', {'tweets': page_obj})


def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})