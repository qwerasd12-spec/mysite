from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="카테고리명")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="슬러그")

    def __str__(self):
        return self.name

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="카테고리")
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    
    # 날짜 및 조회수
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")
    views = models.PositiveIntegerField(default=0, verbose_name="조회수")

    # 파일 및 이미지 첨부
    file = models.FileField(upload_to='board_files/%Y/%m/%d/', blank=True, null=True, verbose_name="첨부파일")
    image = models.ImageField(upload_to='board_images/%Y/%m/%d/', blank=True, null=True, verbose_name="이미지")

    # 비밀글 기능
    is_secret = models.BooleanField(default=False, verbose_name="비밀글 여부")
    password = models.CharField(max_length=100, blank=True, null=True, verbose_name="비밀번호")

    def __str__(self):
        return self.title