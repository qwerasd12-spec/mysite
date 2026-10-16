from django.contrib import admin
from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # 이름을 치면 슬러그가 자동으로 채워지도록 설정

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'created_at', 'views', 'is_secret']
    list_filter = ['category', 'is_secret', 'created_at']
    search_fields = ['title', 'content']