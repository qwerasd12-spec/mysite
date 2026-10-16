from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def post_list(request):
    # 1. 화면에서 전달받은 페이지 번호 (기본값은 1페이지)
    page = request.GET.get('page', '1')
    
    # 2. 화면에서 전달받은 검색어 (없으면 빈 문자열)
    kw = request.GET.get('kw', '')

    # 3. 작성일시가 최신인 순서대로 전체 글 불러오기 (created_at으로 수정)
    post_list = Post.objects.order_by('-created_at')

    # 4. 검색어가 있다면 제목이나 내용에 검색어가 포함된 글만 필터링하기 (subject -> title로 수정)
    if kw:
        post_list = post_list.filter(
            Q(title__icontains=kw) |  # 제목에 검색어가 포함
            Q(content__icontains=kw)    # 또는 내용에 검색어가 포함
        ).distinct()

    # 5. 페이징 처리: 한 페이지에 10개씩 보여주기
    paginator = Paginator(post_list, 10)
    page_obj = paginator.get_page(page)

    # 6. HTML 화면으로 데이터 전달하기
    context = {'post_list': page_obj, 'kw': kw}
    return render(request, 'board/post_list.html', context)

@login_required(login_url='accounts:login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 로그인한 사용자를 작성자로 지정
            post.save()
            return redirect('board:post_list')
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'board/post_form.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    session_key = f'post_{pk}_authenticated'
    is_authorized = request.session.get(session_key, False)
    
    # 비밀글이고, 작성자가 아니며, 아직 인증되지 않은 경우
    if post.is_secret and request.user != post.author and not is_authorized:
        if request.method == 'POST':
            entered_password = request.POST.get('password', '')
            if entered_password == post.password:
                request.session[session_key] = True  # 인증 성공 처리
                return redirect('board:post_detail', pk=pk)
            else:
                error_message = "비밀번호가 틀렸습니다."
                return render(request, 'board/post_detail.html', {'post': post, 'need_password': True, 'error': error_message})
        
        # 비밀번호 입력 폼 렌더링
        return render(request, 'board/post_detail.html', {'post': post, 'need_password': True})
    
    # 일반 글이거나 인증된 경우 조회수 증가 처리 (기존 로직 유지)
    # ... (조회수 중복 방지 로직이 있다면 이 위치에 유지됩니다)
    
    return render(request, 'board/post_detail.html', {'post': post, 'need_password': False})




    post.views +=1
    post.save()

    context = {'post': post}
    return render(request, 'board/post_detail.html', context)

@login_required(login_url='accounts:login')
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # 작성자가 아닐 경우 수정 권한 차단
    if request.user != post.author:
        raise PermissionDenied("수정 권한이 없습니다.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('board:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {'form': form}
    return render(request, 'board/post_form.html', context)

@login_required(login_url='accounts:login')
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # 작성자가 아닐 경우 삭제 권한 차단
    if request.user != post.author:
        raise PermissionDenied("삭제 권한이 없습니다.")

    if request.method == 'POST':
        post.delete()
        return redirect('board:post_list')

    context = {'post': post}
    return render(request, 'board/post_confirm_delete.html', context)

@login_required(login_url='/accounts/login/')
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
    return redirect('board:post_detail', pk=post.id)

@login_required(login_url='/accounts/login/')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        raise PermissionDenied("댓글 삭제 권한이 없습니다.")
    
    post_id = comment.post.id
    comment.delete()
    return redirect('board:post_detail', pk=post_id)