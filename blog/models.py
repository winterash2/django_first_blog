from django.utils import timezone
from django.db import models
from django import forms


# Create your models here.

def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError("제목은 3글자 이상 입력해주세요.")


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[min_length_3_validator])
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    #필드 추가 - 삭제할것
    #test = models.TextField()

    def publish(self):
        # self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title  # 객체주소 대신 글제목을 반환해주는 toSring 함수:;

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    #releated_name을 주면 포스트에 달려있는걸 참조할 때 Post.comments.all() 이런식으로 참조 가능
    #이름을 따로 안 주면 comment마다 다 다르게 알아서 지어버림
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


