from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import auth
from django.contrib.auth.models import User
# Create your views here.
def register(request):
    if request.method=="POST":
        if request.POST['password1']!=request.POST['password2']:
            return render(request, 'register.html', {'message1': '※비밀번호가 일치하지 않습니다.', 'username': request.POST['username'], 'email':request.POST['email']})
        else:
            username=request.POST['username']
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'message2':'※이미 사용중인 ID입니다.', 'username':request.POST['username'], 'email':request.POST['email']})
            else:
                password=request.POST['password1']
                email=request.POST['email']
                User.objects.create_user(username, email, password)
                return render(request, 'main/home.html')
    elif request.method=="GET":
        return render(request, 'register.html')

#def register_done(request):
   # return render(request, 'register_done.html')

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('main')
        else:
            return render(request, 'main/home.html', {'message3': '※존재하지 않는 회원입니다.'})
    

def logout(request):
    auth.logout(request)
    return redirect('home')