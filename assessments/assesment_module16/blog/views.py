from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
from functools import wraps
from .models import Post, Category, Tag, Comment, Like
from .forms import PostForm, CommentForm


def author_required(view_func):
    """Only Authors (and Admins) can access this view. Readers are redirected."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to continue.')
            return redirect('accounts:login')
        if request.user.is_author():
            return view_func(request, *args, **kwargs)
        messages.error(
            request,
            'Only Authors can create or manage posts. '
            'Your account has the Reader role. '
            'Contact an Admin to upgrade your role.'
        )
        return redirect('blog:post_list')
    return _wrapped


def post_list(request):
    posts = Post.objects.filter(status='published').select_related('author', 'category')

    # Filters
    author_filter = request.GET.get('author', '')
    category_filter = request.GET.get('category', '')
    tag_filter = request.GET.get('tag', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search_q = request.GET.get('q', '')

    if author_filter:
        posts = posts.filter(author__username__icontains=author_filter)
    if category_filter:
        posts = posts.filter(category__slug=category_filter)
    if tag_filter:
        posts = posts.filter(tags__slug=tag_filter)
    if date_from:
        try:
            posts = posts.filter(created_at__date__gte=datetime.strptime(date_from, '%Y-%m-%d').date())
        except ValueError:
            pass
    if date_to:
        try:
            posts = posts.filter(created_at__date__lte=datetime.strptime(date_to, '%Y-%m-%d').date())
        except ValueError:
            pass
    if search_q:
        posts = posts.filter(
            Q(title__icontains=search_q) | Q(content__icontains=search_q)
        )

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'author_filter': author_filter,
        'category_filter': category_filter,
        'tag_filter': tag_filter,
        'date_from': date_from,
        'date_to': date_to,
        'search_q': search_q,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(parent__isnull=True).select_related('author')
    is_liked = post.is_liked_by(request.user)
    comment_form = CommentForm()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    comment.parent = Comment.objects.get(id=parent_id, post=post)
                except Comment.DoesNotExist:
                    pass
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('blog:post_detail', slug=slug)

    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'likes_count': post.get_likes_count(),
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)


@author_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save()  # triggers the tags m2m saving
            messages.success(request, 'Post created successfully!')
            if post.status == 'published':
                return redirect('blog:post_detail', slug=post.slug)
            return redirect('blog:my_posts')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})


@author_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            if post.status == 'published':
                return redirect('blog:post_detail', slug=post.slug)
            return redirect('blog:my_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Edit', 'post': post})


@author_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('blog:my_posts')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@author_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/my_posts.html', {'posts': posts})


@login_required
def like_toggle(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': post.get_likes_count()})
    return redirect('blog:post_detail', slug=slug)


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated!')
            return redirect('blog:post_detail', slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {'form': form, 'comment': comment})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_slug = comment.post.slug
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted.')
    return redirect('blog:post_detail', slug=post_slug)
