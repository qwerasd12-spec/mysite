from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'is_secret', 'password', 'image', 'file']
        labels = {
            'category': '카테고리',
            'title': '제목',
            'content': '내용',
            'is_secret': '비밀글 여부',
            'password': '비밀번호 (비밀글인 경우)',
            'image': '이미지 첨부',
            'file': '파일 첨부',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }