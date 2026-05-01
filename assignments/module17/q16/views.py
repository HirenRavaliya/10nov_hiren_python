import requests
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

def github_repos(request):
    repos = []
    error = None
    username = request.GET.get('username', '')
    created_msg = None
    token = settings.GITHUB_TOKEN
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'} if token and token != 'your_github_personal_access_token_here' else {}

    if request.method == 'POST':
        repo_name = request.POST.get('repo_name', '').strip()
        description = request.POST.get('description', '')
        private = request.POST.get('private') == 'on'
        if not token or token == 'your_github_personal_access_token_here':
            error = 'GitHub token not configured. Add GITHUB_TOKEN to .env'
        elif repo_name:
            try:
                resp = requests.post(
                    'https://api.github.com/user/repos',
                    json={'name': repo_name, 'description': description, 'private': private},
                    headers=headers, timeout=10
                )
                if resp.status_code == 201:
                    created_msg = f'Repository "{repo_name}" created successfully!'
                else:
                    error = f'GitHub API error: {resp.json().get("message","Unknown")}'
            except Exception as e:
                error = f'Request failed: {e}'

    if username:
        try:
            resp = requests.get(f'https://api.github.com/users/{username}/repos?sort=updated&per_page=10', headers=headers, timeout=10)
            if resp.status_code == 200:
                repos = resp.json()
            elif resp.status_code == 404:
                error = f'GitHub user "{username}" not found.'
            else:
                error = f'GitHub API error: {resp.status_code}'
        except Exception as e:
            error = f'Request failed: {e}'

    return render(request, 'q16/github.html', {
        'repos': repos, 'error': error, 'username': username, 'created_msg': created_msg,
        'token_configured': bool(token and token != 'your_github_personal_access_token_here'),
    })
