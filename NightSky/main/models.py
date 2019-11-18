from __future__ import unicode_literals
from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your models here.
class Post(models.Model):
    body=models.TextField(default='')
    #pub_date=models.DateTimeField(auto_now_add=True)
    pub_date=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey('auth.User', on_delete=models.CASCADE)
    writer=models.TextField(default='')
    emotion = models.CharField(max_length=255, blank=False)
    image=models.TextField(default='')
    lng=models.TextField(default='')
    lat=models.TextField(default='')
    distinct=models.TextField(default='')
    #lng = models.DecimalField(max_digits = 8, decimal_places = 3, default=Decimal(0))
    #lat = models.DecimalField(max_digits = 8, decimal_places = 3, default=Decimal(0))

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(default='')
    author = models.ForeignKey('auth.user', on_delete=models.CASCADE, default='')
    writer = models.CharField(max_length=255, default='', blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    #created_at = models.DateTimeField(default = timezone.now)

class todayemotion(models.Model):
    emotion=models.TextField(default='')
    to=models.TextField(default='')
    author=models.ForeignKey('auth.User', on_delete=models.CASCADE)

class search(models.Model):
    word=models.TextField(default='')
    author=models.ForeignKey('auth.User', on_delete=models.CASCADE)

class CommentUpdate(UpdateView):
    model = Comment
    fields = [ 'text']
    template_name_suffix = '_update'
    # success_url = '/'


    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
            # 삭제 페이지에서 권한이 없다! 라고 띄우거나
            # detail페이지로 들어가서 삭제에 실패했습니다. 라고 띄우거나
        else:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)

from django.http import HttpResponseRedirect
from django.contrib import messages


class CommentDelete(DeleteView):
    model = Comment
    template_name_suffix = '_delete' 
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(CommentDelete, self).dispatch(request, *args, **kwargs)