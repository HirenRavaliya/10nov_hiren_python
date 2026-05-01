from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileEditForm
from .models import CustomUser, Follow


def register_view(request):
    if request.user.is_authenticated:
        return redirect('blog:post_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # Assign the chosen role group
            chosen_role = form.cleaned_data.get('role', 'Reader')
            group, _ = Group.objects.get_or_create(name=chosen_role)
            user.groups.add(group)
            login(request, user)
            messages.success(request, f'Welcome to WriteSphere, {user.username}! You joined as {chosen_role}.')
            return redirect('blog:post_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('blog:post_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'blog:post_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('blog:post_list')


def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    posts = profile_user.posts.filter(status='published').order_by('-created_at')
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user, following=profile_user
        ).exists()
    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'followers_count': profile_user.get_followers_count(),
        'following_count': profile_user.get_following_count(),
        'posts_count': profile_user.get_posts_count(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def follow_toggle_view(request, username):
    target_user = get_object_or_404(CustomUser, username=username)
    if request.user == target_user:
        messages.warning(request, "You can't follow yourself.")
        return redirect('accounts:profile', username=username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user, following=target_user
    )
    if not created:
        follow.delete()
        messages.info(request, f'You unfollowed {target_user.username}.')
    else:
        messages.success(request, f'You are now following {target_user.username}!')
    return redirect('accounts:profile', username=username)
