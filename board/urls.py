from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/update/', views.post_update, name='post_update'), # 수정 URL
    path('<int:pk>/delete/', views.post_delete, name='post_delete'), # 삭제 URL
    path('comment/create/<int:post_id>/', views.comment_create, name='comment_create'), #댓글
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),#댓글 삭제
]