from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Post, Comment
from .forms import PostModelForm, PostForm, CommentForm
from django.contrib.auth.models import User


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.all()
    name = '안녕하세여'
    return render(request, 'blog/post_list.html', {'posts': posts})
    #return render(request, 'blog/post_list.html')
    #return HttpResponse('''<h1>Django</h1><p>{name}</p>'''.format(name=name))


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new_PostModelForm(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) #여기서 title이랑 text값이 form에 저장됨
            # post.author = request.user #강의 자료에 있던거
            post.author = User.objects.get(username=request.user.username)
            post.published_date = timezone.now() #강의 자료에 있던거
            post.save()
            return redirect('post_detail', pk=post.pk)
    else: #GET 일 때, 빈 폼을 보여주는 부분
        form = PostModelForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            post = Post.objects.create(author=User.objects.get(username=request.user.username),\
                                       published_date=timezone.now(), \
                                       title=form.cleaned_data['title'], \
                                       text=form.cleaned_data['text'])
            # post = form.save(commit=False) #여기서 title이랑 text값이 form에 저장됨
            # # post.author = request.user #강의 자료에 있던거
            # post.author = User.objects.get(username=request.user.username)
            # post.published_date = timezone.now() #강의 자료에 있던거
            # post.save()
            return redirect('post_detail', pk=post.pk)
    else: #GET 일 때, 빈 폼을 보여주는 부분
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk) #DB에서 post 객체 읽어옴
    if request.method == "POST": #수정처리하는 부분
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else: # 수정하기 전에 데이터를 읽어오는 부분
        form = PostModelForm(instance=post) #아까 읽어온 것을 form에 주는 것
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # post id는 이렇게 채워줌
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

