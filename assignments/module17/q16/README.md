# Q16 — GitHub API Integration

## What It Does
- Lists all repositories for a given GitHub username (shows star count, language, description)
- Creates new repositories on GitHub (requires Personal Access Token)

## Endpoint
```
GET /q16/?username=torvalds    — list repos
POST /q16/                     — create repo (needs token)
```

## Setup
1. Create a GitHub Personal Access Token at https://github.com/settings/tokens
2. Add to `.env`:
```
GITHUB_TOKEN=ghp_your_token_here
```

## API Used
```
GET  https://api.github.com/users/{username}/repos
POST https://api.github.com/user/repos
```

## Without Token
- Listing public repos works without a token (lower rate limit)
- Creating repos requires a token with `repo` scope
