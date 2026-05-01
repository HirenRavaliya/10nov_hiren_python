# Q17 — Twitter API Integration (Placeholder)

## Status
**Implementation left blank** — Twitter API v2 now requires a paid subscription for timeline access.

## What It Would Do
Fetch and display the latest 5 tweets from a given Twitter user using the Twitter API v2.

## Required Setup
1. Create Twitter Developer account at https://developer.twitter.com
2. Subscribe to Basic plan ($100/month) for Read access
3. Create a project + app → get Bearer Token
4. Add to `.env`:
```
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

## Implementation
```python
import requests
headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
# Get user ID
user = requests.get(f"https://api.twitter.com/2/users/by/username/{username}", headers=headers)
user_id = user.json()['data']['id']
# Get tweets
tweets = requests.get(f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=5", headers=headers)
```
