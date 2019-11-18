from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, todayemotion, Comment, search
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.core import serializers
import json
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from datetime import datetime
from django.template.loader import render_to_string

# Create your views here.
writer="nothing"

def home(request):
    posts = Post.objects.all
    return render(request, "main/home.html", {'posts_list': posts})

def new(request):

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author=request.user
            post.writer=request.user
            post.published_date=timezone.now()
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, {'form':form})
 

    #def post_edit(request, index):
     #   post = get_object_or_404(Post, pk=index)
      #  if request.method == "POST":
       #     form = PostForm(request.POST, instance=post)
        #    if form.is_valid():
         #       post = form.save(commit=False)
          #      post.author = request.user
           #     post.pub_date = timezone.now()
            #    post.save()
             #   return redirect('post_detail', index=post.pk)
           # else:
            #    form = PostForm(instance=post)
        #return render(request, {'form': form})

def post_edit(request):
    if request.method=="GET":
        pk=request.GET['pk']
        post=get_object_or_404(Post, pk=pk)
        context={'body': post.body, 'date': post.pub_date, 'pk':pk}
        return JsonResponse(context)
    elif request.method=="POST":
        pk=request.POST['pk']
        post=get_object_or_404(Post, pk=pk)
        post.body=request.POST['content']
        post.save()
        return HttpResponse()

def post_delete(request):
    if request.method=="GET":
        pk=request.GET['pk']
        post=get_object_or_404(Post, pk=pk)
        post.delete()
        return HttpResponse()
        #author = request.user
        #posts = Post.objects.filter(author=request.user).order_by('-pub_date')
        #return render(request, 'main/mysky.html', {'posts': posts})
      
def post_remove(request,pk):
    post=get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def main(request):
    return render(request, 'main/main.html')

def comment_create(request, document_id):
    # is_ajax : ajax 기능에 의해 호출된 것인지 구분하기 위한 값
    is_ajax = request.POST.get('is_ajax')

    document = get_object_or_404(Document, pk=document_id)
    comment_form = CommentForm(request.POST)
    comment_form.instance.author_id = request.user.id
    comment_form.instance.document_id = document_id
    if comment_form.is_valid():
        comment = comment_form.save()

    # 만약 ajax에 의해 호출되었다면 redirection 없이 Json 형태로 응답
    if is_ajax:
        # 데이터 만들어서 던져주기
        html = render_to_string('main/mysky.html',{'comment':comment})
        return JsonResponse({'html':html})
    return redirect(reverse('main:detail', args=[document_id]))

def comment_update(request, comment_id):
    is_ajax, data = (request.GET.get('is_ajax'), request.GET) if 'is_ajax' in request.GET else (request.POST.get('is_ajax', False), request.POST)

    comment = get_object_or_404(Comment, pk=comment_id)
    document = get_object_or_404(Document, pk=comment.document.id)

    if request.user != comment.author:
        messages.warning(request, "권한 없음")
    return redirect(document)

    if is_ajax:
        form = CommentForm(data, instance=comment)
        if form.is_valid():
            form.save()
        return JsonResponse({'works':True})

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(document)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'main/comment_update.html', {'form':form})


def comment_delete(request, comment_id):
    is_ajax = request.GET.get('is_ajax') if 'is_ajax' in request.GET else request.POST.get('is_ajax',False)
    comment = get_object_or_404(Comment, pk=comment_id)
    document = get_object_or_404(Document, pk=comment.document.id)

    if request.user != comment.author and not request.user.is_staff and request.user != document.author:
        messages.warning(request, "권한 없음")
        return redirect(document)

    if is_ajax:
        comment.delete()
        return JsonResponse({"works":True})

    if request.method == "POST":
        comment.delete()
        return redirect(document)
    else:
        return render(request, 'main/comment_delete.html', {'object': comment})

def dispatch(self, request, *args, **kwargs):
    object = self.get_object()
    if request.method == "POST":
        super().post(request, *args, **kwargs)
    else:   
        super().post(request, *args, **kwargs)

def mysky(request):
    author = request.user
    posts = Post.objects.filter(author=request.user).order_by('-pub_date')
    if request.method=="POST":
        author=request.user
        body=request.POST['body']
        emotion=request.POST['emo']
        lng=request.POST['x']
        lat=request.POST['y']
        image=request.POST['im']
        pub_date=timezone.now()
        writer=request.user
        Post.objects.create(author=author, body=body, emotion=emotion, lng=lng, lat=lat, image=image, pub_date=pub_date, writer=writer)
        return redirect('mysky')
    else:
        return render(request, 'main/mysky.html', {'posts':posts})
   # if request.method == 'POST':
    #    form = PostForm(request.POST, request.FILES)
     #   if form.is_valid():
      #      post = form.save(commit=False)
       #     post.author=request.user
        #    post.lng=request.POST['x']
         #   post.lat=request.POST['y']
          #  post.save()
           # return redirect('mysky')
    #else:
     #   form = PostForm()
    #return render(request, 'main/mysky.html', {'posts':posts, 'form':form})

def realmain(request):
    if request.method=="POST":
        em=request.POST['emo']
        posts=Post.objects.filter(emotion=em)
        today=todayemotion.objects.filter(author=request.user)
        if today:
            today=todayemotion.objects.get(author=request.user)
            today.emotion=em
            today.save()
        else:
            author=request.user
            emotion=em
            todayemotion.objects.create(author=author, emotion=emotion)
        paginator=Paginator(posts, 100)
        page=request.GET.get('page')
        pages=paginator.get_page(page)
        return render(request, 'main/realmain.html', {'posts':posts, 'pages':pages})
    else:
        today=todayemotion.objects.get(author=request.user)
        em=today.emotion
        posts=Post.objects.filter(emotion=em)
        paginator=Paginator(posts, 100)
        page=request.GET.get('page')
        pages=paginator.get_page(page)
        return render(request, 'main/realmain.html', {'posts':posts, 'pages':pages})

def user_update(request):
    user=get_object_or_404(User, username=request.user.username)
    posts=Post.objects.filter(author=request.user)
    comments=Comment.objects.filter(author=request.user)
    return render(request, 'main/user_update.html', {'user':user, 'posts':posts, 'comments':comments,})
def change_Email(request):
        if request.method=="POST":
                newemail=request.POST['NEWEMAIL']
                user=get_object_or_404(User, username=request.user.username)
                user.email=newemail
                user.save()
                #return render(request, 'user_update.html', {'message3':'※이메일이 변경되었습니다.'})
                return redirect('user_update')
def change_ID(request):
        if request.method=="POST":
                newID=request.POST['NEWID']
                current_password=request.POST['origin']
                user=User.objects.get(username=request.user.username)
                if check_password(current_password, user.password):
                    if User.objects.filter(username=newID).exists():
                        return render(request, 'main/user_update.html', {'message4':'※이미 사용중인 ID입니다.'})
                    else:
                        user=User.objects.get(username=request.user.username)
                        user.username=newID
                        user.save()
                        auth.logout(request)
                        return redirect('home')
                else:
                    return render(request, 'main/user_update.html', {'message':'※원래 비밀번호가 아닙니다.'})

def change_pw(request):
    if request.method == "POST":
        current_password = request.POST['origin']
        user = User.objects.get(username=request.user.username)
        if check_password(current_password, user.password):
            new_password = request.POST['password1']
            password_confirm = request.POST['password2']
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.logout(request)
                return redirect('home')
            else:
                return render(request, 'main/user_update.html', {'message2':'※비밀번호가 일치하지 않습니다.'})
        else:
                return render(request, 'main/user_update.html', {'message':'※원래 비밀번호가 아닙니다.'})

def mysearch(request):
    if request.method=="POST":
        word=request.POST['word']
        post=Post.objects.filter(body__icontains=word)|Post.objects.filter(emotion__icontains=word)|Post.objects.filter(writer__icontains=word)
        sear=search.objects.filter(author=request.user)
        if sear:
            sear=search.objects.get(author=request.user)
            sear.word=word
            sear.save()
        else:
            author=request.user
            search.objects.create(author=author, word=word)
        paginator=Paginator(post, 100)
        page=request.GET.get('page')
        pages=paginator.get_page(page)
        return render(request, 'main/realmain.html', {'posts':post, 'pages':pages})
    else:
        sear=search.objects.get(author=request.user)
        word=sear.word
        post=Post.objects.filter(body__icontains=word)|Post.objects.filter(emotion__icontains=word)|Post.objects.filter(writer__icontains=word)
        paginator=Paginator(post, 100)
        page=request.GET.get('page')
        pages=paginator.get_page(page)
        return render(request, 'main/realmain.html', {'posts':post, 'pages':pages})
    

"""
def postdetail(request, index):
    post = get_object_or_404(Post, pk=index)
    if request.method =='POST':
        form=CommentForm(request.POST)
        if form.is_valid:
            comment=form.save(commit=False)
            comment.author=request.user
            comment.post=post
            comment.save()
            return redirect('post_detail', index=post.pk)
    else:
        form=CommentForm()
        comments=Comment.objects.filter(post=post)
        return render(request, 'main/mysky.html', {'form':form, 'postdetail':post, 'comments':comments})
"""
def post_total(request):
    if request.method=="GET":
        pk=request.GET['pk']
        post=get_object_or_404(Post, pk=pk)
        pk=post.pk
        context={'body':post.body, 'date': post.pub_date, 'writer':post.writer, 'pk':pk}
        return JsonResponse(context)

def postdetail(request):
        if request.method=="GET":
            pk=request.GET['pk'] 
            post=get_object_or_404(Post, pk=pk)
            comments=Comment.objects.filter(post=post)
            data=[]
            for comment in comments:
                data.append(comment.content)
                time=str(comment.created_at.replace(microsecond=0))
                datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                data.append(time)
                data.append(comment.writer)
            context={'comments': data }
            return JsonResponse(context)
        elif request.method=="POST":
            pk=request.POST['postpk']
            post=get_object_or_404(Post, pk=pk)
            author=request.user
            writer=request.user
            created_at=timezone.now()
            content=request.POST['content']
            Comment.objects.create(writer=writer, content=content, post=post, created_at=created_at, author=author)
            return HttpResponse()


def othersky(request, index):
    originpk=index
    post=get_object_or_404(Post, pk=index)
    author=post.author
    posts=Post.objects.filter(author=author)
    return render(request, 'main/other_sky.html', {'posts':posts, 'author':author, 'otherpk':originpk})

def commentothersky(request, index):
    originwriter=index
    posts=Post.objects.filter(writer=index)
    return render(request, 'main/other_sky.html', {'posts':posts, 'author':originwriter})
    
def otherdetail(request):
    if request.method=="GET":
        pk=request.GET['pk']
        post=get_object_or_404(Post, pk=pk)
        context={'body': post.body, 'date': post.pub_date, 'pk':pk}
        return JsonResponse(context)
